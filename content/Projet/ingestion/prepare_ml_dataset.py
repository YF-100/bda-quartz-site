#!/usr/bin/env python3
"""
Entraînement du modèle de prédiction Bitcoin - Version Simplifiée
Utilise uniquement les données de prix (7 ans d'historique)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🚀 PRÉPARATION DES DONNÉES POUR ML")
print("="*70)

# 1. Charger les données
print("\n[1/5] Chargement des données prix (7 ans)...")
df = pd.read_csv('data/prices/btc_1h_data_2018_to_2025.csv')
print(f"  ✓ {len(df):,} lignes chargées")

# 2. Nettoyer et préparer
print("\n[2/5] Nettoyage des données...")

# Identifier les colonnes
if 'Open time' in df.columns:
    # Format Binance
    df['timestamp'] = pd.to_datetime(df['Open time'])
    df['close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['high'] = pd.to_numeric(df['High'], errors='coerce')
    df['low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['volume'] = pd.to_numeric(df['Volume'], errors='coerce')
else:
    # Format CoinGecko (timestamps)
    df['timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    df['close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['high'] = pd.to_numeric(df['High'], errors='coerce')
    df['low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['volume'] = pd.to_numeric(df['Volume'], errors='coerce')

# Supprimer les NaN
df = df.dropna(subset=['close', 'timestamp'])
df = df.sort_values('timestamp')
df = df.reset_index(drop=True)

print(f"  ✓ {len(df):,} lignes valides après nettoyage")

# 3. Créer les features
print("\n[3/5] Création des features...")

# Features de prix
df['returns'] = df['close'].pct_change()
df['log_returns'] = np.log(df['close'] / df['close'].shift(1))

# Moyennes mobiles
for window in [7, 30, 90]:
    df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
    df[f'ma_ratio_{window}'] = df['close'] / df[f'ma_{window}']

# Volatilité
df['volatility_7'] = df['returns'].rolling(window=7).std()
df['volatility_30'] = df['returns'].rolling(window=30).std()

# Momentum
df['momentum_7'] = df['close'] - df['close'].shift(7)
df['momentum_30'] = df['close'] - df['close'].shift(30)

# High-Low spread
df['hl_spread'] = (df['high'] - df['low']) / df['close']

# Volume features (si disponible)
if df['volume'].notna().sum() > 100:
    df['volume_ma_7'] = df['volume'].rolling(window=7).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma_7']

# Patterns temporels
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['day_of_month'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month

# 4. Créer la variable cible
print("\n[4/5] Création de la variable cible...")

# Prédire si le prix va monter dans les N prochaines heures
prediction_horizon = 24  # 24 heures

df['future_price'] = df['close'].shift(-prediction_horizon)
df['target'] = (df['future_price'] > df['close']).astype(int)
df['target_change_pct'] = ((df['future_price'] - df['close']) / df['close']) * 100

# 5. Finaliser le dataset
print("\n[5/5] Finalisation...")

# Supprimer les NaN créés par les shifts
df = df.dropna()

# Sélectionner les features finales
feature_columns = [
    'close', 'returns', 'log_returns',
    'ma_7', 'ma_30', 'ma_90',
    'ma_ratio_7', 'ma_ratio_30', 'ma_ratio_90',
    'volatility_7', 'volatility_30',
    'momentum_7', 'momentum_30',
    'hl_spread',
    'hour', 'day_of_week', 'day_of_month', 'month'
]

# Ajouter volume si disponible
if 'volume_ratio' in df.columns and df['volume_ratio'].notna().sum() > 100:
    feature_columns.extend(['volume', 'volume_ma_7', 'volume_ratio'])

# Dataset final
df_final = df[['timestamp'] + feature_columns + ['target', 'target_change_pct']].copy()

# Sauvegarder
output_file = 'data/ml_dataset_ready.csv'
df_final.to_csv(output_file, index=False)

print(f"\n{'='*70}")
print("✅ DATASET ML PRÊT!")
print(f"{'='*70}")
print(f"📁 Fichier: {output_file}")
print(f"📊 Lignes: {len(df_final):,}")
print(f"📋 Features: {len(feature_columns)}")
print(f"🎯 Variable cible: target (0=baisse, 1=hausse)")
print(f"⏰ Horizon: {prediction_horizon} heures")
print()
print(f"📅 Période:")
print(f"   De: {df_final['timestamp'].min()}")
print(f"   À:  {df_final['timestamp'].max()}")
print()
print(f"📈 Distribution cible:")
baisse = (df_final['target'] == 0).sum()
hausse = (df_final['target'] == 1).sum()
print(f"   Baisse: {baisse:,} ({baisse/len(df_final)*100:.1f}%)")
print(f"   Hausse: {hausse:,} ({hausse/len(df_final)*100:.1f}%)")
print()
print(f"💡 PROCHAINES ÉTAPES:")
print(f"   1. Diviser en train/validation/test (70/15/15)")
print(f"   2. Entraîner un modèle (Logistic Regression, Random Forest, etc.)")
print(f"   3. Évaluer les performances")
print(f"{'='*70}")

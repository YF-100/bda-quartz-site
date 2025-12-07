"""
Traite les données blockchain échantillonnées avec PySpark
Crée des métriques agrégées par jour pour enrichir le dataset de prix
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, max as spark_max, 
    min as spark_min, stddev, from_unixtime, to_date, lit
)
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, ArrayType
import json
from pathlib import Path

def create_spark_session():
    """Initialise Spark avec config optimisée"""
    return SparkSession.builder \
        .appName("BlockchainSampleProcessing") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .getOrCreate()

def load_sampled_blocks(spark, data_dir):
    """
    Charge tous les blocks échantillonnés
    Extrait les transactions et les métriques
    """
    
    data_path = Path(data_dir)
    block_files = sorted(data_path.glob("block_nov*.json"))
    
    if not block_files:
        raise FileNotFoundError(f"Aucun fichier trouvé dans {data_dir}")
    
    print(f"📂 Chargement de {len(block_files)} blocks...")
    
    all_transactions = []
    block_metrics = []
    
    for block_file in block_files:
        with open(block_file, 'r') as f:
            block = json.load(f)
        
        block_hash = block.get('hash')
        block_height = block.get('height')
        block_time = block.get('time')
        block_size = block.get('size', 0)
        
        transactions = block.get('tx', [])
        
        # Métriques du block
        block_metrics.append({
            'block_hash': block_hash,
            'block_height': block_height,
            'block_time': block_time,
            'num_transactions': len(transactions),
            'block_size_bytes': block_size
        })
        
        # Extrait chaque transaction
        for tx in transactions:
            tx_data = {
                'block_hash': block_hash,
                'block_height': block_height,
                'block_time': block_time,
                'tx_hash': tx.get('hash'),
                'size': tx.get('size', 0),
                'weight': tx.get('weight', 0),
                'fee': tx.get('fee', 0),
                'inputs_count': len(tx.get('inputs', [])),
                'outputs_count': len(tx.get('out', []))
            }
            
            # Calcule valeur totale des outputs
            total_value = sum(out.get('value', 0) for out in tx.get('out', []))
            tx_data['total_value'] = total_value
            
            all_transactions.append(tx_data)
    
    # Crée DataFrames Spark
    tx_df = spark.createDataFrame(all_transactions)
    blocks_df = spark.createDataFrame(block_metrics)
    
    print(f"   ✅ {tx_df.count():,} transactions chargées")
    print(f"   ✅ {blocks_df.count()} blocks traités")
    
    return tx_df, blocks_df

def compute_daily_metrics(tx_df, blocks_df):
    """
    Agrège les métriques par jour
    Crée des features pour enrichir le dataset de prix
    """
    
    print("\n📊 Calcul des métriques quotidiennes...")
    
    # Convertit timestamp en date
    tx_with_date = tx_df.withColumn(
        'date',
        to_date(from_unixtime(col('block_time')))
    )
    
    blocks_with_date = blocks_df.withColumn(
        'date',
        to_date(from_unixtime(col('block_time')))
    )
    
    # Métriques sur les transactions
    tx_metrics = tx_with_date.groupBy('date').agg(
        count('tx_hash').alias('total_transactions'),
        spark_sum('total_value').alias('total_volume_satoshis'),
        avg('total_value').alias('avg_tx_value_satoshis'),
        spark_sum('fee').alias('total_fees_satoshis'),
        avg('fee').alias('avg_fee_satoshis'),
        spark_max('fee').alias('max_fee_satoshis'),
        spark_min('fee').alias('min_fee_satoshis'),
        stddev('fee').alias('stddev_fee_satoshis'),
        avg('inputs_count').alias('avg_inputs_per_tx'),
        avg('outputs_count').alias('avg_outputs_per_tx'),
        spark_sum('size').alias('total_tx_size_bytes'),
        avg('size').alias('avg_tx_size_bytes')
    )
    
    # Métriques sur les blocks
    block_metrics = blocks_with_date.groupBy('date').agg(
        count('block_hash').alias('num_blocks_sampled'),
        spark_sum('block_size_bytes').alias('total_block_size_bytes'),
        avg('block_size_bytes').alias('avg_block_size_bytes')
    )
    
    # Joint les deux
    daily_metrics = tx_metrics.join(block_metrics, on='date', how='inner')
    
    # Convertit en BTC (1 BTC = 100,000,000 satoshis)
    daily_metrics = daily_metrics.withColumn(
        'total_volume_btc',
        col('total_volume_satoshis') / 100000000
    ).withColumn(
        'avg_tx_value_btc',
        col('avg_tx_value_satoshis') / 100000000
    ).withColumn(
        'total_fees_btc',
        col('total_fees_satoshis') / 100000000
    ).withColumn(
        'avg_fee_btc',
        col('avg_fee_satoshis') / 100000000
    )
    
    # Trie par date
    daily_metrics = daily_metrics.orderBy('date')
    
    return daily_metrics

def save_results(daily_metrics, output_dir):
    """Sauvegarde les résultats en CSV et Parquet"""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # CSV pour analyse facile
    csv_file = output_path / "blockchain_daily_metrics_november.csv"
    daily_metrics.coalesce(1).write.mode('overwrite').option('header', True).csv(str(csv_file))
    print(f"\n💾 Métriques quotidiennes sauvegardées:")
    print(f"   • CSV: {csv_file}")
    
    # Parquet pour performance
    parquet_file = output_path / "blockchain_daily_metrics_november.parquet"
    daily_metrics.write.mode('overwrite').parquet(str(parquet_file))
    print(f"   • Parquet: {parquet_file}")
    
    # Affiche un aperçu
    print("\n📊 Aperçu des métriques quotidiennes:")
    daily_metrics.select(
        'date',
        'total_transactions',
        'total_volume_btc',
        'avg_fee_btc',
        'num_blocks_sampled'
    ).show(10, truncate=False)
    
    # Stats globales
    print("\n📈 Statistiques globales pour novembre:")
    daily_metrics.agg(
        spark_sum('total_transactions').alias('total_tx'),
        spark_sum('total_volume_btc').alias('total_volume_btc'),
        spark_sum('total_fees_btc').alias('total_fees_btc'),
        avg('avg_fee_btc').alias('avg_daily_fee_btc')
    ).show(truncate=False)

def main():
    print("="*70)
    print("⚡ TRAITEMENT SPARK - BLOCKCHAIN ÉCHANTILLONNÉE NOVEMBRE 2025")
    print("="*70)
    print()
    
    # Initialise Spark
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    # Chemins
    input_dir = "data/blockchain_sample_november"
    output_dir = "data/processed"
    
    try:
        # Charge les données
        tx_df, blocks_df = load_sampled_blocks(spark, input_dir)
        
        # Calcule métriques quotidiennes
        daily_metrics = compute_daily_metrics(tx_df, blocks_df)
        
        # Sauvegarde
        save_results(daily_metrics, output_dir)
        
        print("\n" + "="*70)
        print("✅ TRAITEMENT TERMINÉ")
        print("="*70)
        print()
        print("💡 PROCHAINE ÉTAPE:")
        print("   Joindre ces métriques avec les prix horaires pour le ML")
        print()
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()

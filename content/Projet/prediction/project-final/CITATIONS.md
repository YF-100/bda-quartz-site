# Citations and References

**Project:** Bitcoin Price Prediction using PySpark  
**Course:** Big Data Analytics (BDA) 2025-2026  
**Institution:** ESIEE Paris

---

## Datasets

### 1. Bitcoin Historical Data (mczielinski)

**Source:** Kaggle  
**Dataset:** `mczielinski/bitcoin-historical-data`  
**URL:** https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data  
**License:** CC0: Public Domain  
**Description:** Bitcoin historical data with 1-minute OHLCV data from 2012 to 2025  
**Usage:** Used for price data preprocessing and technical indicator generation

**Citation:**
```
mczielinski. (2017). Bitcoin Historical Data. Kaggle. 
https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data
```

### 2. Bitcoin Network On-Chain Blockchain Data

**Source:** Kaggle  
**Dataset:** `Bitcoin Network On-Chain Blockchain Data`  
**URL:** https://www.kaggle.com/datasets/aleexharris/bitcoin-network-on-chain-blockchain-data/data?select=blockchain_dot_com_column_desc.csv
  

## Software and Libraries

### Apache Spark

**Name:** Apache Spark  
**Version:** 3.5.0 / 4.0.1  
**License:** Apache License 2.0  
**URL:** https://spark.apache.org/  
**Usage:** Distributed data processing and machine learning

**Citation:**
```
Apache Spark. (2024). Apache Spark - Unified Engine for Large-Scale Data Analytics.
https://spark.apache.org/
```

### PySpark

**Name:** PySpark  
**Version:** 3.5.0 / 4.0.1  
**License:** Apache License 2.0  
**URL:** https://spark.apache.org/docs/latest/api/python/  
**Usage:** Python API for Apache Spark

**Citation:**
```
PySpark Documentation. (2024). PySpark API Documentation.
https://spark.apache.org/docs/latest/api/python/
```

### Python Libraries

#### pandas
**Name:** pandas  
**License:** BSD License  
**URL:** https://pandas.pydata.org/  
**Usage:** Data manipulation and analysis

#### NumPy
**Name:** NumPy  
**License:** BSD License  
**URL:** https://numpy.org/  
**Usage:** Numerical computing

#### PyYAML
**Name:** PyYAML  
**License:** MIT License  
**URL:** https://pyyaml.org/  
**Usage:** YAML configuration file parsing

#### matplotlib / seaborn
**Name:** matplotlib, seaborn  
**License:** BSD License  
**URL:** https://matplotlib.org/, https://seaborn.pydata.org/  
**Usage:** Data visualization (optional)

---

## Bitcoin Core

**Name:** Bitcoin Core  
**License:** MIT License  
**URL:** https://bitcoin.org/en/bitcoin-core/  
**Usage:** Blockchain data source (planned, not yet used)  
**Note:** Currently, blockchain data synchronization is pending. When used, Bitcoin Core will be used to download and parse blockchain blocks.

**Citation:**
```
Bitcoin Core. (2024). Bitcoin Core - Bitcoin Full Node Implementation.
https://bitcoin.org/en/bitcoin-core/
```

---

## References and Documentation

### Technical Indicators

The following technical indicators were implemented based on standard financial analysis:

- **Moving Averages (MA):** Simple moving average calculation
- **RSI (Relative Strength Index):** Wilder's RSI formula
- **MACD (Moving Average Convergence Divergence):** Standard MACD calculation
- **Bollinger Bands:** Standard deviation-based bands
- **ROC (Rate of Change):** Percentage change calculation

**Reference:**
```
Technical Analysis of the Financial Markets. John J. Murphy. New York Institute of Finance, 1999.
```

### Time Series Cross-Validation

**Method:** Time-based split (no random shuffle)  
**Rationale:** Prevents data leakage in time series prediction tasks  
**Reference:**
```
Hyndman, R. J., & Athanasopoulos, G. (2021). Forecasting: principles and practice (3rd ed.).
OTexts. https://otexts.com/fpp3/
```

---

## Acknowledgments

- **Kaggle** for providing open datasets
- **Apache Spark** community for excellent documentation and tools
- **ESIEE Paris** for course guidance and support

---

## License

This project is for educational purposes as part of the BDA course at ESIEE Paris.

All datasets used are publicly available under CC0: Public Domain or similar licenses.

All software libraries used are open-source and used in accordance with their respective licenses.

---

**Last Updated:** 2025-12-07


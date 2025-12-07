# Environment Summary

## System Information

- **OS**: macOS 24.6.0 (Darwin)
- **Python**: 3.12.6
- **Java**: OpenJDK 17.0.17
- **Spark**: 4.0.1 (detected from practice4 environment)
- **PySpark**: 4.0.1

## Spark Configuration

### Key Settings

- `spark.sql.session.timeZone`: UTC
- `spark.sql.shuffle.partitions`: 4 (for local development)
- Log level: WARN

### Application Names

- **Part A**: BDA-Assignment04-PartA-Relational
- **Part B**: BDA-Assignment04-PartB-Streaming

## Data Directories

```
Assignment4/
├── data/
│   ├── tpch/
│   │   ├── TPC-H-0.1-TXT/          # Pipe-delimited text files
│   │   │   ├── customer.tbl
│   │   │   ├── lineitem.tbl
│   │   │   ├── nation.tbl
│   │   │   ├── orders.tbl
│   │   │   ├── part.tbl
│   │   │   ├── partsupp.tbl
│   │   │   ├── region.tbl
│   │   │   └── supplier.tbl
│   │   └── TPC-H-0.1-PARQUET/      # Parquet format
│   │       ├── customer/
│   │       ├── lineitem/
│   │       ├── nation/
│   │       ├── orders/
│   │       ├── part/
│   │       └── supplier/
│   └── taxi-data/                   # NYC Taxi CSV files
│       ├── part-2015-12-01-0000.csv
│       ├── part-2015-12-01-0001.csv
│       └── ... (1400+ files)
```

## Output Directories

```
Assignment4/
├── outputs/
│   ├── q1.txt                       # A1: Count results
│   ├── q2.txt                       # A2: Clerk-order pairs
│   ├── q3.txt                       # A3: Part-supplier pairs
│   ├── q4/                          # A4: Nation aggregations (CSV)
│   ├── q5/                          # A5: Monthly volumes (CSV)
│   ├── q6/                          # A6: Pricing summary (CSV)
│   ├── q7/                          # A7: Top 10 orders (CSV)
│   ├── hourly_trip_count/           # B1: Hourly counts (Parquet)
│   ├── region_trip_count/           # B2: Region counts (Parquet)
│   └── trending_arrivals/           # B3: Trending windows (Parquet + status files)
├── checkpoints/
│   ├── hourly_trip_count/
│   ├── region_trip_count/
│   └── trending_arrivals/
└── proof/
    ├── plan_q1_parquet.txt
    ├── plan_q5_multijoin.txt
    ├── PART_A_SUMMARY.md
    └── PART_B_SUMMARY.md
```

## Dependencies

### Python Packages

- pyspark==4.0.1
- py4j (bundled with PySpark)

### System Requirements

- Java 8 or higher (tested with OpenJDK 17)
- Python 3.7 or higher (tested with Python 3.12)
- Sufficient disk space for data and outputs (~500MB)

## Performance Notes

### Local Execution

- Configured for local development with `spark.sql.shuffle.partitions=4`
- For production/cluster execution, increase shuffle partitions based on data size
- Recommended: Set shuffle partitions to 2-3× number of CPU cores

### Memory Settings

Default Spark memory settings should suffice for the 0.1 scale factor dataset:
- Driver memory: 1g (default)
- Executor memory: 1g (default)

For larger datasets, adjust via:
```bash
spark-submit --driver-memory 4g --executor-memory 4g ...
```

## Reproducibility

All queries are deterministic given the same input data and Spark version. Results may vary slightly across different Spark versions due to optimization changes, but should be consistent within the same version.

---

Generated: 2025-12-05


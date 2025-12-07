---
title: ENV
---

# Environment Documentation

## Assignment
Big Data Analytics — Assignment 01
Date: November 12, 2025

## Versions
- **Python**: 3.14.0
- **PySpark/Spark**: 4.0.1
- **OS**: Darwin 24.3.0 (arm64)
- **Java**: openjdk version "21.0.1" 2023-10-17
OpenJDK Runtime Environment (build 21.0.1+12-29)
OpenJDK 64-Bit Server VM (build 21.0.1+12-29, mixed mode, sharing)


## Key Spark Configurations
- `spark.app.id`: local-1762961593573
- `spark.app.name`: BDA-A01
- `spark.app.startTime`: 1762961593057
- `spark.app.submitTime`: 1762961592925
- `spark.driver.extraJavaOptions`: -Djava.net.preferIPv6Addresses=false -XX:+IgnoreUnrecognizedVMOptions --add-modules=jdk.incubator.vector --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED -Djdk.reflect.useDirectMethodHandle=false -Dio.netty.tryReflectionSetAccessible=true
- `spark.driver.host`: 192.168.216.22
- `spark.driver.port`: 51041
- `spark.executor.extraJavaOptions`: -Djava.net.preferIPv6Addresses=false -XX:+IgnoreUnrecognizedVMOptions --add-modules=jdk.incubator.vector --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED -Djdk.reflect.useDirectMethodHandle=false -Dio.netty.tryReflectionSetAccessible=true
- `spark.executor.id`: driver
- `spark.hadoop.fs.s3a.vectored.read.max.merged.size`: 2M
- `spark.hadoop.fs.s3a.vectored.read.min.seek.size`: 128K
- `spark.master`: local[*]
- `spark.rdd.compress`: True
- `spark.serializer.objectStreamReset`: 100
- `spark.sql.artifact.isolation.enabled`: false
- `spark.sql.session.timeZone`: UTC
- `spark.sql.shuffle.partitions`: 8
- `spark.sql.warehouse.dir`: file:/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/bigdata/lab1/spark-warehouse
- `spark.submit.deployMode`: client
- `spark.submit.pyFiles`: 
- `spark.ui.port`: 4040
- `spark.ui.showConsoleProgress`: true

## Execution Environment
- **Mode**: Local (single machine)
- **Shuffle Partitions**: 8
- **Timezone**: UTC
- **Spark UI**: http://localhost:4040

## Dataset
- **Source**: Shakespeare corpus (~5 MB)
- **Path**: `data/shakespeare.txt`
- **Lines**: 112710

## Parameters
- **PMI Threshold (K)**: 3
- **Max tokens per line**: 40
- **Perfect followers min count**: > 1

## Deliverables
- `outputs/perfect_followers.csv`
- `outputs/pmi_pairs_sample.csv`
- `outputs/pmi_stripes_sample.csv`
- `proof/plan_perfect.txt`
- `proof/plan_pmi_pairs.txt`
- `proof/plan_pmi_stripes.txt`
- Spark UI screenshots (manual capture required)
- `lab_metrics_log.csv` (Spark UI metrics)

## Reproducibility Notes
1. Install PySpark: `pip install pyspark`
2. Ensure Java 8+ is installed
3. Run notebook cells in order
4. Capture Spark UI metrics during execution
5. Access Spark UI at http://localhost:4040 while jobs are running

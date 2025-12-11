---
date: 2025-12-07
---

# BDA-A01 — Environment & Reproducibility

Below is the exact environment used to run this assignment.

```json
{
  "timestamp_utc": "2025-10-23T08:30:34.353746+00:00",
  "os": {
    "platform": "macOS-15.3.1-arm64-arm-64bit",
    "machine": "arm64",
    "python": "3.12.7 (main, Oct 23 2025, 09:34:49) [Clang 17.0.0 (clang-1700.0.13.5)]"
  },
  "java": {
    "JAVA_HOME": "<unset>",
    "java_version": "/Users/yassinf/.bash_profile: line 2: nvm: command not found\n/Users/yassinf/.bash_profile: line 3: nvm: command not found\nopenjdk version \"21.0.1\" 2023-10-17\nOpenJDK Runtime Environment (build 21.0.1+12-29)\nOpenJDK 64-Bit Server VM (build 21.0.1+12-29, mixed mode, sharing)"
  },
  "spark": {
    "spark_version": "4.0.0",
    "pyspark_version": "4.0.0",
    "SPARK_HOME": "<pip-only>",
    "spark_conf": {
      "spark.app.id": "local-1761206932666",
      "spark.app.name": "BDA-A01",
      "spark.app.startTime": "1761206932156",
      "spark.app.submitTime": "1761206931509",
      "spark.driver.extraJavaOptions": "-Djava.net.preferIPv6Addresses=false -XX:+IgnoreUnrecognizedVMOptions --add-modules=jdk.incubator.vector --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED -Djdk.reflect.useDirectMethodHandle=false -Dio.netty.tryReflectionSetAccessible=true",
      "spark.driver.host": "192.168.219.197",
      "spark.driver.port": "56349",
      "spark.executor.extraJavaOptions": "-Djava.net.preferIPv6Addresses=false -XX:+IgnoreUnrecognizedVMOptions --add-modules=jdk.incubator.vector --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/jdk.internal.ref=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.base/sun.nio.cs=ALL-UNNAMED --add-opens=java.base/sun.security.action=ALL-UNNAMED --add-opens=java.base/sun.util.calendar=ALL-UNNAMED --add-opens=java.security.jgss/sun.security.krb5=ALL-UNNAMED -Djdk.reflect.useDirectMethodHandle=false -Dio.netty.tryReflectionSetAccessible=true",
      "spark.executor.id": "driver",
      "spark.hadoop.fs.s3a.vectored.read.max.merged.size": "2M",
      "spark.hadoop.fs.s3a.vectored.read.min.seek.size": "128K",
      "spark.master": "local[*]",
      "spark.rdd.compress": "True",
      "spark.serializer.objectStreamReset": "100",
      "spark.sql.artifact.isolation.enabled": "false",
      "spark.sql.session.timeZone": "UTC",
      "spark.sql.shuffle.partitions": "8",
      "spark.sql.warehouse.dir": "file:/Users/yassinf/Documents/Documents-Mac/ESIEE/E5/bigdata/spark-warehouse",
      "spark.submit.deployMode": "client",
      "spark.submit.pyFiles": "",
      "spark.ui.showConsoleProgress": "true"
    }
  },
  "packages": {
    "pyarrow": "21.0.0",
    "pandas": "2.3.3"
  }
}
```

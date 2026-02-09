# ⚠ Environment Setup Issues & Resolutions (Windows + PySpark + Delta)

This project was developed on Windows 10 using local PySpark + JupyterLab (not Databricks).
During setup, multiple non-trivial issues were encountered related to Spark, Hadoop, Delta Lake, and Windows native dependencies.

This section documents those issues and their resolutions for future reference.


---

## 1. SparkSession Not Intializied (`NoneType` Error)
### Issue
```text
AttributeError: 'NoneType' object has no attribute 'createDataFrame'
```
### Root Cause
The helper function get_spark_session() was defined but did not return the SparkSession object, causing `spark` to be `None`

### Resolution
Ensure the function explicitly returns `spark`
```python
def get_spark_session():
    spark = SparkSession.builder.getOrCreate()
    return spark
```

---

## 2. Delta Lake Not Found (`DATA_SOURCE_NOT_FOUND)
### Issue
```text
Failed to find the data source: delta
ClassNotFoundException: delta.DefaultSource
```
### Root Cause
Although `delta-spark` was installed via `pip`, the Delta Lake JAR was not attached to Spark's classpath.
This happens in open-source Spark (Databricks does this automatically).

### Resolution
Use Delta's official helper to configure Spark:
```python
from delta import configure_spark_with_delta_pip

builder = SparkSession.builder.appName("NYC Taxi Analytics")
spark = configure_spark_with_delta_pip(builder).getOrCreate()
```
---

## 3. Spark-Delta Version Incompatibility
#### Issue
```text
NoClassDefFoundError: org/apache/spark/sql/catalyst/expressions/TimeAdd
```

#### Root Cause
Mismatch between:
- `pyspark` version
- `delta-spark` version

Delta Lake relies on internal Spark classes, so version alignment is mandatory.

#### Resolution
Downgraded to a known compatible combinations:
```bash
pip install pyspark==3.4.1
pip install delta-spark==2.4.0
```

Verified with:
```python
import pyspark, delta
print(pyspark.__version__)
print(delta.__version__)
```
---

## 4. Haddop Native I/O Errors on Windows
#### Issues (Repeated for both Delta & Parquet)
```text
UnsatisfiedLinkError:
org.apache.hadoop.io.nativeio.NativeIO$Windows.access0
```
#### Root Cause
On Windows, Spark uses Hadoop native filesystem calls.
The required native binaries were missing or incomplete, causing *all filesystem writes* to fail (Delta and Parquet)

Initially:
- `winutils.exe` was present
- but `hadoop.dll` was missing

#### Resolution (Critical Fix):
Placed both required native binaries in Hadoop's `bin` directory:
```makefile
C:\hadoop\bin\
├── winutils.exe
└── hadoop.dll
```
Set environment variables:
```text
HADOOP_HOME = C:\hadoop
PATH += C:\hadoop\bin
```
After restarting all terminals and Jupyter, filesystem writes worked successfully.

---

## 5. Why this happens on Windows(Context)
- Spark was designed primarily for Linux-based environments
- Hadoop native filesystem support on Windows is partial
- Delta Lake intensively uses filesystem metadata operations (`_delta_log`)
- Missing native libraries cause low-level JVM errors.

This is why platforms like Databricks, Linux, WSL, Docker, or cloud storage are preferred in production.

---

## 6. Final Working Spark Session Configuration
```python
import os
from pathlib import Path


# Set HADOOP_HOME first
os.environ['HADOOP_HOME'] = 'C:\\hadoop'
hadoop_bin = Path('C:/hadoop/bin')
if str(hadoop_bin) not in os.environ['PATH']:
    os.environ['PATH'] = str(hadoop_bin) + os.pathsep + os.environ['PATH']


# Importing PySpark
from pyspark.sql import SparkSession, Row
from delta import configure_spark_with_delta_pip


def get_spark_session(app_name: str = "NYC Taxi Analytics Platform"):
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.driver.extraJavaOptions", "-Djava.library.path=C:/hadoop/bin")
        .config("spark.executor.extraJavaOptions", "-Djava.library.path=C:/hadoop/bin")
        .config("spark.sql.shuffle.partitions", "4")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
```
---

## 7. Key Learnings
- Delta Lake requires strict Spark version compatibility
- On Windows, both `winutils.exe` and `hadoop.dll` are required
- Many Spark filesystem errors are OS-level, not code-level
- Databricks abstracts away these issues by running on Linux

---

## 8. Note for Reviewers
This project intentionally uses local PySpark to demonstrate:
- Hands-on debugging ability
- Understanding of Spark-Hadoop-Delta internals
- Real-world environment troubleshooting skills

The same pipelines can run unchanged on Databricks or Linux-based Spark clusters.

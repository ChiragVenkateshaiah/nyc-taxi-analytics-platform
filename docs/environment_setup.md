# ⚙ Environment Setup
## PySpark + Delta Lake + JupyterLab (Local)
This guide sets up a local Lakehouse-style environment using open-source tools to build the NYC Taxi Analytic Platform.

---

### 1. Prerequisites
#### System Requirements
- OS: Windows/macOS/Linux
- Python: 3.9 or 3.10 (recommended)
- RAM: 8 GB minimum (16GB ideal)

Check Python:
```bash
python --version
```

---

### 2. Create a Virtual Environment (Strong Recommended)
Using Conda (Best for Spark on Windows)
```
conda create -n pyspark_env python=3.9 -y
conda activate pyspark_env
```
---

### 3. Install Required Libraries
#### Core Packages
```bash
pip install pyspark
pip install delta-spark
pip install jupyterlab
pip install pandas pyarrow
```

Optional (nice to have):
```bash
pip install ipykernel
```

---

### 4. Register the Environment in Jupyter
```bash
python -m ipykernel install --user --name pyspark_env --display-name "PySpark Lakehouse"
```
Start Jupyterlab:
```
jupyter lab
```
Select kernel: pyspark(Conda)

---

### 5. Create Spark Session with Delta Support
Create a reusable file:
```bash
notebooks/utils/spark_session.py
```

```python
from pyspark.sql import SparkSession

def get_spark_session(app_name: str = "NYC Taxi Analytics Platform"):
    spark = (
        SparkSession.builder
        .appName(app_name)
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension"
        )

        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )

        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark
```
Usage in notebooks:
```python
from utils.spark_session import get_spark_session

spark = get_spark_session()
```

---

### 6. Project Directory Layout (Local Lakehouse)
```bash
data/
├── bronze/
├── silver/
└── gold/
```
Each folder will contain Delta tables.

```bash
data/bronze/nyc_taxi_trips/
data/silver/nyc_taxi_trips/
data/gold/gold_revenue_metrics/
```

---

### 7. Verify Delta Lake is Working
#### Test Notebook: `notebooks/test_delta_setup.ipynb`
```python
from pyspark.sql import Row
from utils.spark_session import get_spark_session

spark = get_spark_session()

df = spark.createDataFrame([
    Row(id=1, value="test"),
    Row(id=2, value="delta")
])

df.write.format("delta").mode("overwrite").save("data/bronze/delta_test")

df_read = spark.read.format("delta").load("data/bronze/delta_test")
df_read.show()
```
If this works, Lakehouse is ready.

---

### 8. Spark Configuration Notes
- Local mode: `spark.master = local[*]`
- Delta provides:
      - Acide transactions
      - Schema enforcement
      - Time travel
- Same config work on Databricks with minimal changes

---

### 9. Common Issues & Fixes
#### Java Not Found
Set `JAVA_HOME`

#### PySpark Version Conflicts
Ensure:
```bash
pip show pyspark
pip show delta-spark
```
They should be compatible (Spark 3.x)


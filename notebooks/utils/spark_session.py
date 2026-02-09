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

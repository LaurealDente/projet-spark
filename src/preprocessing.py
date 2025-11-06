from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.sql.functions import col
from config import *

def create_preprocessing_pipeline():
    """
    Crée le pipeline de preprocessing
    """
    # Assembler les features
    assembler = VectorAssembler(
        inputCols=FEATURE_COLS,
        outputCol="features_raw"
    )
    
    # Normalisation
    scaler = StandardScaler(
        inputCol="features_raw",
        outputCol="features",
        withMean=True,
        withStd=True
    )
    
    pipeline = Pipeline(stages=[assembler, scaler])
    
    return pipeline

def describe_data(df):
    """Affiche des statistiques sur les données"""
    print("\n=== EXPLORATION DES DONNÉES ===")
    df.printSchema()
    
    fraud_count = df.filter(col("Class") == 1).count()
    normal_count = df.filter(col("Class") == 0).count()
    fraud_ratio = fraud_count / df.count() * 100
    
    print(f"Total: {df.count()} transactions")
    print(f"Normales: {normal_count} ({100-fraud_ratio:.2f}%)")
    print(f"Frauduleuses: {fraud_count} ({fraud_ratio:.2f}%)")
    
    df.describe().show()

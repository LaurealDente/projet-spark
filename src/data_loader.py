from pyspark.sql import SparkSession
from config import *
import os

def load_data(spark: SparkSession, use_sample: bool = False):
    """
    Charge le dataset Credit Card Fraud
    
    Args:
        spark: SparkSession
        use_sample: Si True, utilise seulement les 10% premiers
    
    Returns:
        DataFrame Spark
    """
    if not DATASET_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_FILE}")
    
    print(f"Chargement du dataset: {DATASET_FILE}")
    
    df = spark.read.csv(str(DATASET_FILE), header=True, inferSchema=True)
    
    if use_sample:
        print("Mode sample: utilisation de 10% du dataset")
        df = df.sample(0.1, seed=RANDOM_SEED)
    
    print(f"Dataset chargé: {df.count()} lignes, {len(df.columns)} colonnes")
    
    return df

def prepare_splits(df):
    """Split train/test"""
    train, test = df.randomSplit([TRAIN_TEST_SPLIT, 1-TRAIN_TEST_SPLIT], 
                                  seed=RANDOM_SEED)
    train.cache()
    test.cache()
    
    print(f"Train: {train.count()} lignes")
    print(f"Test: {test.count()} lignes")
    
    return train, test

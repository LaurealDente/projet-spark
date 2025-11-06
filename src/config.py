from pathlib import Path
import os

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models" / "trained_models"
RESULTS_DIR = PROJECT_ROOT / "results"

# Dataset
DATASET_URL = "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud"
DATASET_FILE = RAW_DATA_DIR / "creditcard.csv"

# Spark Configuration
SPARK_MASTER = os.getenv("SPARK_MASTER", "local[*]")
SPARK_EXECUTOR_CORES = int(os.getenv("SPARK_EXECUTOR_CORES", "2"))
SPARK_EXECUTOR_MEMORY = os.getenv("SPARK_EXECUTOR_MEMORY", "2g")
SPARK_NUM_EXECUTORS = int(os.getenv("SPARK_NUM_EXECUTORS", "1"))

# ML Configuration
TRAIN_TEST_SPLIT = 0.8
RANDOM_SEED = 42
CV_FOLDS = 3

# Feature Engineering
FEATURE_COLS = [f"V{i}" for i in range(1, 29)]  # V1-V28 PCA features
LABEL_COL = "Class"

print(f"Project Root: {PROJECT_ROOT}")
print(f"Data Dir: {DATA_DIR}")

#!/bin/bash

echo "========================================="
echo "Lancement du Pipeline Spark (Mode Local)"
echo "========================================="

# Activer l'environnement
source ~/spark-env/bin/activate
# Ou si vous utilisez Mamba: mamba activate spark-fraud-detection

# Créer les répertoires de données
mkdir -p data/raw data/processed results models/trained_models

# Télécharger les données (si nécessaire)
if [ ! -f "data/raw/creditcard.csv" ]; then
    echo "Téléchargement du dataset..."
    python scripts/download_data.sh
fi

# Lancer le pipeline
python -c "
from pyspark.sql import SparkSession
from src.config import *
from src.data_loader import load_data, prepare_splits
from src.preprocessing import describe_data
from src.model_trainer import train_model, make_predictions
from src.evaluator import evaluate_model

# Créer la session Spark
spark = SparkSession.builder \
    .appName('FraudDetection_Local') \
    .master('local[*]') \
    .getOrCreate()

# Pipeline complet
df = load_data(spark, use_sample=False)
describe_data(df)

train, test = prepare_splits(df)
model = train_model(train, test, use_tuning=False)
predictions = make_predictions(model, test)
metrics = evaluate_model(predictions)

# Sauvegarder les résultats
import json
with open('results/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print('\\n✓ Pipeline complété avec succès!')

spark.stop()
"

echo "========================================="
echo "Résultats sauvegardés dans results/"
echo "========================================="

#!/bin/bash

# ===================================================================
# SCRIPT DE LANCEMENT DU PIPELINE EN MODE LOCAL NATIF (SANS DOCKER)
# ===================================================================

echo "🚀 Lancement du pipeline Spark en mode local natif..."

# 1. Activer l'environnement Conda/Mamba
# Assurez-vous que le nom de l'environnement est correct
source /home/laureal/miniforge3/bin/activate spark-fraud-detection
if [ $? -ne 0 ]; then
    echo "❌ Erreur: Impossible d'activer l'environnement Mamba 'spark-fraud-detection'."
    echo "   Veuillez vérifier qu'il est bien créé avec 'mamba env create -f environment.yml'"
    exit 1
fi
echo "✓ Environnement 'spark-fraud-detection' activé."

# 2. Définir la configuration Spark pour le mode local
# 'local[*]' dit à Spark d'utiliser autant de threads que de cœurs CPU disponibles.
export SPARK_MASTER="local[*]"
# On alloue une partie de la RAM de votre machine au driver Spark.
export SPARK_DRIVER_MEMORY="4g" 

export PYSPARK_SUBMIT_ARGS='--conf "spark.driver.extraJavaOptions=--add-opens=java.base/java.lang=ALL-UNNAMED" pyspark-shell'

echo "✓ Configuration Spark définie pour le mode 'local[*]'"

# 3. Lancer le script Python du pipeline
# Le script 'fraud_detection_pipeline.py' lira les variables d'environnement
# pour configurer sa session Spark.
echo "▶️  Exécution du script Python 'src/fraud_detection_pipeline.py'..."
python src/fraud_detection_pipeline.py

# Vérifier le code de sortie du script Python
if [ $? -eq 0 ]; then
  echo "✅ Pipeline terminé avec succès en mode local."
else
  echo "❌ Le pipeline a échoué en mode local." >&2
fi

unset PYSPARK_SUBMIT_ARGS

echo "👋 Fin du script de lancement."

#!/bin/bash

# ==============================================================================
# Script de Démarrage pour les conteneurs Spark Master et Worker
# ==============================================================================

# Charge les variables d'environnement de Spark (SPARK_HOME, etc.)
. "/opt/spark/bin/load-spark-env.sh"

# ------------------------------------------------------------------------------
# Logique de Démarrage en fonction du Rôle du Conteneur
# ------------------------------------------------------------------------------

# Vérifie la variable d'environnement SPARK_WORKLOAD, qui est définie
# dans le fichier docker-compose.yml.
if [ "$SPARK_WORKLOAD" == "master" ]; then

  echo "🚀 Démarrage du conteneur en mode MASTER..."

  # Lance le processus Master de Spark.
  $SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master \
    --ip $SPARK_MASTER_HOST \
    --port $SPARK_MASTER_PORT \
    --webui-port $SPARK_MASTER_WEBUI_PORT >> $SPARK_MASTER_LOG 2>&1

elif [ "$SPARK_WORKLOAD" == "worker" ]; then

  echo "⚙️ Démarrage du conteneur en mode WORKER..."
  echo "Connexion au master : $SPARK_MASTER"

  # Lance le processus Worker de Spark.
  $SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker \
    --webui-port $SPARK_WORKER_WEBUI_PORT \
    $SPARK_MASTER >> $SPARK_WORKER_LOG 2>&1

elif [ "$SPARK_WORKLOAD" == "submit" ]; then

  echo "SUBMITTING SPARK JOB"
  spark-submit $@

else
  echo "❌ Type de workload non défini : '$SPARK_WORKLOAD'. Doit être 'master', 'worker' ou 'submit'."
  exit 1
fi

#!/bin/bash

# ===================================================================
# SCRIPT DE LANCEMENT D'UN CLUSTER SPARK TEMPORAIRE
# ===================================================================
# Ce script s'exécute à l'intérieur de l'allocation Slurm.

# -- Étape 1 : Configuration de l'Environnement Spark --

# S'assurer que les variables d'environnement de Spark sont bien chargées
# (normalement fait par `module load spark`).
if [ -z "$SPARK_HOME" ]; then
  echo "Erreur : SPARK_HOME n'est pas défini. Le module Spark a-t-il été chargé ?" >&2
  exit 1
fi

# Définir des répertoires temporaires pour les logs et les PID de Spark.
# Il est préférable d'utiliser le répertoire /tmp ou un scratch space.
export SPARK_LOG_DIR=/tmp/spark-logs-$USER-$$
export SPARK_PID_DIR=/tmp/spark-pids-$USER-$$
mkdir -p $SPARK_LOG_DIR
mkdir -p $SPARK_PID_DIR


# -- Étape 2 : Démarrage du Master Spark --

# Récupérer la liste des noms d'hôtes alloués par Slurm.
NODES=$(scontrol show hostnames $SLURM_JOB_NODELIST)
# Le premier nœud de la liste sera notre master.
MASTER_NODE=$(echo "$NODES" | head -n 1)

echo "--- Démarrage du Master Spark sur le nœud : $MASTER_NODE ---"
# Se connecte en SSH au nœud master pour y lancer le script de démarrage du master.
# Le script 'start-master.sh' est fourni par Spark.
ssh $MASTER_NODE "$SPARK_HOME/sbin/start-master.sh"

# Petite pause pour laisser le temps au service master de démarrer complètement.
sleep 10


# -- Étape 3 : Démarrage des Workers Spark --

# Construire l'URL du master que les workers devront contacter.
SPARK_MASTER_URL="spark://$MASTER_NODE:7077"
echo "URL du Master Spark : $SPARK_MASTER_URL"

# Récupérer la liste des nœuds restants pour les workers.
WORKER_NODES=$(echo "$NODES" | tail -n +2)

for node in $WORKER_NODES; do
  echo "--- Démarrage d'un Worker Spark sur le nœud : $node ---"
  # Se connecte en SSH à chaque nœud worker pour y lancer le script de démarrage
  # d'un worker, en lui passant l'URL du master.
  ssh $node "$SPARK_HOME/sbin/start-worker.sh $SPARK_MASTER_URL"
done

echo "Cluster Spark démarré avec succès. Attente de la connexion des workers..."
sleep 10 # Attendre que les workers s'enregistrent auprès du master.


# -- Étape 4 : Soumission de l'Application Spark --

echo "--- Soumission du job Python 'fraud_detection_pipeline.py' ---"

# Utilise `spark-submit` pour lancer l'application.
# Les paramètres comme le master, la mémoire, etc., sont spécifiés ici.
# Le code de votre application se trouve dans le répertoire courant.
# Assurez-vous que le chemin vers votre script est correct.
spark-submit \
  --master $SPARK_MASTER_URL \
  --deploy-mode client \
  --driver-memory 3g \
  --num-executors 3 \
  --executor-memory 4g \
  --executor-cores 8 \
  ./src/fraud_detection_pipeline.py # Assurez-vous que ce chemin est correct

# $? contient le code de sortie de la dernière commande. Si différent de 0, il y a eu une erreur.
if [ $? -eq 0 ]; then
  echo "Application Spark terminée avec succès."
else
  echo "Erreur lors de l'exécution de l'application Spark." >&2
fi


# -- Étape 5 : Nettoyage --

echo "--- Arrêt du cluster Spark temporaire ---"
# Utilise le script 'stop-all.sh' pour arrêter proprement tous les
# processus master et workers sur tous les nœuds.
$SPARK_HOME/sbin/stop-all.sh

echo "Nettoyage des répertoires temporaires."
rm -rf $SPARK_LOG_DIR
rm -rf $SPARK_PID_DIR

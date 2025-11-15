#!/bin/bash -l

# ===================================================================
# SCRIPT DE SOUMISSION SLURM POUR UN CLUSTER SPARK
# ===================================================================

# -- Paramètres du Job SBATCH --

#SBATCH --job-name=spark_fraud_detection
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

# -- Exécution du Script --

echo "========================================================="
echo "  DÉMARRAGE DU JOB SPARK SUR LE CLUSTER SLURM"
# ... (le reste du fichier est inchangé) ...


echo "Chargement des modules..."
module purge
module load java/11
module load spark/3.4.1
module load python/3.11
echo "Modules chargés."

echo "Lancement du script de déploiement du cluster Spark..."
srun ./slurm/launch_spark_cluster.sh

echo "========================================================="
echo "  LE JOB SLURM EST TERMINÉ"
echo "========================================================="

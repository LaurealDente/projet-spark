# Instructions d'Installation et d'Exécution

## Prérequis

- Ubuntu 22.04 ou supérieur
- 16 GB RAM minimum
- 30 GB espace disque

## Installation Locale

### 1. Cloner le dépôt
git clone https://github.com/LaurealDente/projet-spark.git
cd projet-spark

### 2. Installer Mamba
conda install -c conda-forge mamba

### 3. Créer l'environnement
mamba env create -f environment.yml
mamba activate spark-fraud-detection

### 4. Télécharger les données
mkdir -p data/raw
cd data/raw

## Exécution Locale avec Docker
### Démarrer le cluster
cd docker
docker-compose build
docker-compose up -d
Attendre que les services soient prêts
docker-compose ps

### Accéder aux UIs
- Master UI: http://localhost:8080
- Worker 1 UI: http://localhost:8081
- Worker 2 UI: http://localhost:8082
- Worker 3 UI: http://localhost:8083

### Soumettre un job
bash scripts/run_local.sh

### Arrêter le cluster
cd docker
docker-compose down

## Exécution sur Slurm (Cluster Académique)
### 1. Transférer le projet
scp -r sprojet-spark alauret@tsp-client:~/

### 2. Vérifier les ressources disponibles
sinfo
sacctmgr show assoc where user=$USER

### 3. Soumettre le job
sbatch slurm/submit_spark.slurm

### 4. Suivre l'exécution
squeue -u $USER
tail -f spark_job_*.out

### 5. Récupérer les résultats
scp user@cluster.edu:~/spark-bigdata-fraud-detection/results/* ./results/

## Résultats
Les résultats sont sauvegardés dans `results/`:
- `metrics.json` : Métriques de performance
- `confusion_matrix.png` : Matrice de confusion
- `roc_curve.png` : Courbe ROC
- `training_logs.txt` : Logs d'entraînement
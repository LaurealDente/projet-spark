# Architecture du Projet

## Vue d'ensemble

Ce projet implémente un pipeline de **détection de fraude par carte bancaire** utilisant:
- **Apache Spark** pour le traitement distribué de données (284K transactions)
- **Spark MLlib** pour le Machine Learning
- **Docker** et **Docker-Compose** pour développement local
- **Slurm** pour exécution sur cluster HPC académique
- **Python** pour l'orchestration et la science des données

## Architecture Système

### Mode Développement (Local)
Laptop
├── Docker Master (Spark Master)
├── Docker Worker 1
├── Docker Worker 2
└── Docker Worker 3


### Mode Production (Slurm)
Slurm Cluster
├── Nœud 1 (Master Spark)
├── Nœud 2 (Worker Spark)
├── Nœud 3 (Worker Spark)
└── Nœud 4 (Worker Spark)



## Pipeline ML

1. **Ingestion** : Chargement du CSV (284K lignes, 30 colonnes)
2. **Exploration** : Analyse de déséquilibre (99.8% normales, 0.2% frauduleuses)
3. **Prétraitement** : Normalisation StandardScaler
4. **Feature Engineering** : VectorAssembler sur 28 features PCA
5. **Entraînement** : Random Forest (50-200 arbres)
6. **Évaluation** : AUC-ROC, Precision-Recall, F1-Score
7. **Sauvegarde** : Modèle en Parquet

## Flux de Données

creditcard.csv (60 MB)
↓
Spark Read CSV
↓
DataFrame (284K rows)
↓
StandardScaler
↓
Random Forest (100 étapes d'entraînement)
↓
Predictions
↓
Metrics & Model Artifacts


## Configurations par Environnement

| Paramètre | Local | Slurm | Cloud |
|-----------|-------|-------|-------|
| Executor Memory | 2 GB | 28 GB | 32 GB |
| Num Executors | 1 | 3 | 10 |
| Executor Cores | 4 | 8 | 8 |
| Shuffle Partitions | 100 | 200 | 500 |
| Temps Max | Illimité | 1h | Illimité |

## Technologie Stack

- **Spark 3.5.1** : Moteur de traitement distribué
- **Python 3.11** : Langage de programmation
- **Mamba** : Gestion des environnements
- **Docker** : Conteneurisation
- **Slurm** : Gestionnaire de ressources HPC
- **Git** : Versioning du code
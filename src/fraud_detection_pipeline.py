import time
import argparse
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Importe les modules que vous avez créés
from config import *
from data_loader import load_data, prepare_splits
from preprocessing import create_preprocessing_pipeline, describe_data
from model_trainer import train_model, make_predictions
from evaluator import evaluate_model

def main(args):
    """
    Pipeline complet pour la détection de fraude.
    """
    # --- AJOUT: Démarrer le chronomètre global ---
    pipeline_start_time = time.time()
    
    print("=" * 70)
    print(f"  DÉMARRAGE DU PIPELINE (Mode: {args.suffix})")
    print("=" * 70)

    # 1. Création de la SparkSession
    print("\n[1/6] Initialisation de la session Spark...")
    spark_builder = SparkSession.builder \
        .appName(f"FraudDetectionPipeline-{args.suffix}") \
        .config("spark.driver.extraJavaOptions", "--add-opens=java.base/java.lang=ALL-UNNAMED") \
        .config("spark.executor.extraJavaOptions", "--add-opens=java.base/java.lang=ALL-UNNAMED")

    if args.suffix == 'local':
        spark_builder = spark_builder.master("local[*]").config("spark.driver.memory", "4g")

    spark = spark_builder.getOrCreate()
    sc = spark.sparkContext
    print(f"✓ Session Spark initialisée (Version: {sc.version}, Master: {sc.master})")

    # 2. Chargement des données
    print("\n[2/6] Chargement et préparation des données...")
    initial_df = load_data(spark)
    train_df, test_df = prepare_splits(initial_df)
    describe_data(train_df)

    # 3. Entraînement du modèle
    print("\n[3/6] Entraînement du modèle de Machine Learning...")
    # --- AJOUT: Chronomètre pour l'entraînement ---
    training_start_time = time.time()
    pipeline_model = train_model(train_df, test_df, use_tuning=False)
    training_end_time = time.time()
    training_duration = training_end_time - training_start_time
    print(f"✓ Modèle entraîné en {training_duration:.2f} secondes.")

    # 4. Évaluation du modèle
    print("\n[4/6] Évaluation des performances du modèle...")
    predictions_df = make_predictions(pipeline_model, test_df)
    metrics = evaluate_model(predictions_df)
    
    # --- AJOUT: Calcul du temps total et ajout aux métriques ---
    pipeline_end_time = time.time()
    total_duration = pipeline_end_time - pipeline_start_time
    
    metrics['total_execution_time_seconds'] = round(total_duration, 2)
    metrics['training_time_seconds'] = round(training_duration, 2)
    
    print(f"✓ Temps d'exécution total (calculs) : {total_duration:.2f} secondes.")
    # -------------------------------------------------------------

    # 5. Sauvegarde des résultats et du modèle
    print("\n[5/6] Sauvegarde des résultats et des artefacts...")
    metrics_path = f"{RESULTS_DIR}/metrics_{args.suffix}.json"
    model_path = f"{MODELS_DIR}/fraud_detection_model_{args.suffix}.spark"
    
    try:
        import json
        import os
        os.makedirs(RESULTS_DIR, exist_ok=True)
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"✓ Métriques sauvegardées dans : {metrics_path}")
    except Exception as e:
        print(f"⚠️ Avertissement : Impossible de sauvegarder les métriques. Erreur : {e}")

    try:
        pipeline_model.write().overwrite().save(model_path)
        print(f"✓ Modèle sauvegardé dans : {model_path}")
    except Exception as e:
        print(f"⚠️ Avertissement : Impossible de sauvegarder le modèle. Erreur : {e}")

    # 6. Arrêt
    print("\n[6/6] Arrêt de la session Spark...")
    spark.stop()

    print("\n" + "=" * 70)
    print("  ✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer le pipeline de détection de fraude.")
    parser.add_argument(
        '--suffix',
        type=str,
        default='local',
        help="Suffixe pour les fichiers de sortie (ex: 'local', 'docker', 'slurm')."
    )
    parsed_args = parser.parse_args()
    main(parsed_args)

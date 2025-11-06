from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from preprocessing import create_preprocessing_pipeline
from config import *
import time

def train_model(train_df, test_df, use_tuning=False):
    """
    Entraîne le modèle Random Forest
    """
    print("\n=== ENTRAÎNEMENT DU MODÈLE ===")
    
    # Preprocessing pipeline
    preprocessing_pipeline = create_preprocessing_pipeline()
    
    # Modèle
    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol=LABEL_COL,
        numTrees=50,
        maxDepth=10,
        seed=RANDOM_SEED,
        numPartitions=100
    )
    
    # Pipeline complet
    full_pipeline = Pipeline(stages=[*preprocessing_pipeline.getStages(), rf])
    
    if use_tuning:
        print("Hyperparameter tuning activé...")
        
        param_grid = ParamGridBuilder() \
            .addGrid(rf.numTrees, [30, 50, 100]) \
            .addGrid(rf.maxDepth, [5, 10, 15]) \
            .build()
        
        evaluator = BinaryClassificationEvaluator(
            labelCol=LABEL_COL,
            rawPredictionCol="rawPrediction",
            metricName="areaUnderROC"
        )
        
        cv = CrossValidator(
            estimator=full_pipeline,
            estimatorParamMaps=param_grid,
            evaluator=evaluator,
            numFolds=CV_FOLDS
        )
        
        start = time.time()
        model = cv.fit(train_df)
        elapsed = time.time() - start
        
        print(f"Cross-Validation completed in {elapsed:.2f}s")
        print(f"Best AUC: {cv.avgMetrics[0]:.4f}")
        
        model = model.bestModel
    else:
        print("Entraînement simple (pas de tuning)...")
        start = time.time()
        model = full_pipeline.fit(train_df)
        elapsed = time.time() - start
        print(f"Entraînement completed in {elapsed:.2f}s")
    
    return model

def make_predictions(model, test_df):
    """Fait les prédictions sur le test set"""
    predictions = model.transform(test_df)
    return predictions

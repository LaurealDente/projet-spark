from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col
from config import *

def evaluate_model(predictions):
    """
    Évalue le modèle avec plusieurs métriques
    """
    print("\n=== ÉVALUATION DU MODÈLE ===")
    
    # AUC-ROC
    evaluator_auc = BinaryClassificationEvaluator(
        labelCol=LABEL_COL,
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = evaluator_auc.evaluate(predictions)
    
    # AUC-PR
    evaluator_pr = BinaryClassificationEvaluator(
        labelCol=LABEL_COL,
        rawPredictionCol="rawPrediction",
        metricName="areaUnderPR"
    )
    pr = evaluator_pr.evaluate(predictions)
    
    print(f"AUC-ROC: {auc:.4f}")
    print(f"AUC-PR: {pr:.4f}")
    
    # Matrice de confusion
    print("\nMatrice de Confusion:")
    predictions.groupBy(LABEL_COL, "prediction").count().show()
    
    # Statistiques par classe
    tp = predictions.filter((col(LABEL_COL) == 1) & (col("prediction") == 1)).count()
    fp = predictions.filter((col(LABEL_COL) == 0) & (col("prediction") == 1)).count()
    tn = predictions.filter((col(LABEL_COL) == 0) & (col("prediction") == 0)).count()
    fn = predictions.filter((col(LABEL_COL) == 1) & (col("prediction") == 0)).count()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\nPrecision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    return {
        "auc_roc": auc,
        "auc_pr": pr,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

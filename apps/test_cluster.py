import time
from pyspark.sql import SparkSession

def main():
    """
    Script principal pour tester le cluster Spark.
    """
    print("=" * 60)
    print(" DÉBUT DU TEST DE CLUSTER SPARK")
    print("=" * 60)

    # 1. Création de la SparkSession
    # Le .master() n'est pas nécessaire ici car il sera fourni
    # par la commande `spark-submit`.
    print("\n[1/5] Création de la session Spark...")
    spark = SparkSession.builder \
        .appName("ClusterTest") \
        .getOrCreate()
    
    sc = spark.sparkContext
    
    print(f"✓ Session Spark créée.")
    print(f"    - Version de Spark : {sc.version}")
    print(f"    - URL du Master    : {sc.master}")
    print(f"    - App Name         : {sc.appName}")
    print(f"    - App ID           : {sc.applicationId}")

    # 2. Test de Calcul Parallèle avec un RDD
    print("\n[2/5] Test de calcul distribué (RDD)...")
    
    # Création d'un RDD avec 12 partitions pour forcer la distribution
    # sur plusieurs workers.
    data = range(10_000_000)
    rdd = sc.parallelize(data, numSlices=12)
    
    print(f"✓ RDD créé avec {rdd.getNumPartitions()} partitions.")

    start_time = time.time()
    # Exécution d'une action pour déclencher le calcul
    total_sum = rdd.map(lambda x: x * 2).sum()
    end_time = time.time()
    
    print(f"✓ Calcul terminé en {end_time - start_time:.3f} secondes.")
    print(f"    - Résultat du calcul : {total_sum}")
    # Résultat attendu: 99999990000000

    # 3. Test de DataFrame
    print("\n[3/5] Test de traitement de données (DataFrame)...")
    
    df_data = [(i, f"cat_{i % 100}") for i in range(100_000)]
    df = spark.createDataFrame(df_data, ["id", "category"])

    print(f"✓ DataFrame créé avec {df.count()} lignes.")
    print(f"    - Partitions du DataFrame : {df.rdd.getNumPartitions()}")

    start_time = time.time()
    # Exécution d'une agrégation distribuée
    category_counts = df.groupBy("category").count().collect()
    end_time = time.time()

    print(f"✓ Agrégation terminée en {end_time - start_time:.3f} secondes.")
    print(f"    - Nombre de catégories trouvées : {len(category_counts)}")

    # 4. Test d'Écriture sur le Volume Partagé
    print("\n[4/5] Test d'écriture sur le volume partagé...")
    
    output_path = "/opt/workspace/data/test_output.parquet"
    try:
        df.write.mode("overwrite").parquet(output_path)
        print(f"✓ DataFrame sauvegardé avec succès dans '{output_path}'")
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture : {e}")
        spark.stop()
        exit(1)

    # 5. Test de Lecture depuis le Volume Partagé
    print("\n[5/5] Test de lecture depuis le volume partagé...")
    
    try:
        read_df = spark.read.parquet(output_path)
        print(f"✓ Fichier Parquet lu avec succès.")
        print(f"    - Nombre de lignes lues : {read_df.count()}")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
        spark.stop()
        exit(1)

    print("\n" + "=" * 60)
    print(" ✅ TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
    print(" ✅ Votre cluster Spark est opérationnel.")
    print("=" * 60)

    # Arrêt de la session Spark
    spark.stop()


if __name__ == "__main__":
    main()

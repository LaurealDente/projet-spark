# Utiliser une image de base Ubuntu stable
FROM ubuntu:22.04

# Définir des arguments pour éviter les questions interactives pendant l'installation
ARG DEBIAN_FRONTEND=noninteractive

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    git \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Définir les variables d'environnement pour Spark
ENV SPARK_VERSION=3.5.1
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python

# Installation de Spark - C'EST LA LIGNE CORRIGÉE
# On télécharge le binaire standard pour Hadoop 3, sans variable HADOOP_VERSION
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# Copier les fichiers de l'application depuis le contexte de build
COPY requirements.txt /tmp/
COPY start-spark.sh /

# Installation des dépendances Python
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Rendre le script de démarrage exécutable
RUN chmod +x /start-spark.sh

# Définir le répertoire de travail par défaut
WORKDIR /opt/workspace

# Définir le point d'entrée du conteneur
ENTRYPOINT ["/start-spark.sh"]

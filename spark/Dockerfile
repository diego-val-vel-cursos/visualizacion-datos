# Base image with Java
FROM openjdk:11.0.11-jre-slim-buster

# Install necessary packages for running Spark and Python with Plotly
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    wget \
    software-properties-common \
    ssh \
    net-tools \
    ca-certificates \
    python3 \
    python3-pip \
    python3-numpy \
    python3-matplotlib \
    python3-scipy \
    python3-pandas \
    python3-simpy \
    && pip3 install plotly

# Set Python3 as the default Python version
RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Set the fixed value for PYTHONHASHSEED (necessary for Python 3.3+)
ENV PYTHONHASHSEED=1

# Define Spark and Hadoop versions
ENV SPARK_VERSION=3.0.2 \
    HADOOP_VERSION=3.2 \
    SPARK_HOME=/opt/spark

# Download and install Spark
RUN wget --no-verbose -O apache-spark.tgz \
    "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz" \
    && mkdir -p /opt/spark \
    && tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
    && rm apache-spark.tgz

# Set Spark environment variables
ENV SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_LOG_DIR=/opt/spark/logs \
    SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
    SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
    SPARK_WORKER_WEBUI_PORT=8080 \
    SPARK_WORKER_PORT=7000 \
    SPARK_MASTER="spark://spark-master:7077"

# Expose Spark ports
EXPOSE 8080 7077 6066

# Setup log directory and permissions
RUN mkdir -p $SPARK_LOG_DIR && \
    touch $SPARK_MASTER_LOG && \
    touch $SPARK_WORKER_LOG && \
    ln -sf /dev/stdout $SPARK_MASTER_LOG && \
    ln -sf /dev/stdout $SPARK_WORKER_LOG

# Copy the start script
COPY start-spark.sh /start-spark.sh
RUN chmod +x /start-spark.sh

# Set the default command to execute when creating a new container
CMD ["/bin/bash", "/start-spark.sh"]

#!/bin/bash

# Carga las variables de entorno de Spark
. /opt/spark/bin/load-spark-env.sh

# Decide qué hacer basado en la variable de entorno SPARK_WORKLOAD
case "$SPARK_WORKLOAD" in
  master)
    export SPARK_MASTER_HOST=`hostname`
    /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master \
      --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT
    ;;
  worker)
    /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker \
      --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER
    ;;
  *)
    echo "Undefined Workload Type $SPARK_WORKLOAD, must specify: master, worker"
    ;;
esac

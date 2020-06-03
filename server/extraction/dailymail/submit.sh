PYSPARK_DRIVER_PYTHON=/home/hduser/anaconda3/envs/fake_news/bin/python3 \
PYSPARK_PYTHON=./environment/bin/python3 \
spark-submit \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/home/hduser/environment/bin/python3 \
--master yarn \
--deploy-mode client \
--archives /home/hduser/environment.tar.gz#environment \
--num-executors 2 \
--executor-memory 3840m \
--executor-cores 8 \
--driver-memory 2048m \
/home/hduser/extraction/dailymail/extraction_dailymail.py

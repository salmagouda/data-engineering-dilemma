-gcloud auth login
-bq --project_id ny-rides-sal extract -m ny_taxi.tip_model gs://nyc_ml_model/tip_model
-mkdir /tmp/model
-gsutil -m cp -r gs://nyc_ml_model/tip_model tmp/model
-mkdir -p serving_dir/tip_model/1
-cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
-docker pull tensorflow/serving
-docker pull emacski/tensorflow-serving:latest
-docker run -p 8501:8501 --mount type=bind,source=/home/sal/git/data-engineering-dilemma/module3/serving_dir/tip_model,target= /models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &

-docker run -p 8501:8501 \ --mount type=bind,source=`pwd`/serving_dir tip_model/,target=/models/tip_model \ -e MODEL_NAME=tip_model tensorflow/serving

docker run -p 8501:8501 --network="host" --mount type=bind,source=`pwd`/serving_dir/tip_model,target=/models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &

docker run --rm -ti \
    -w /code -v $PWD:/code \
    -v /var/run/docker.sock:/var/run/docker.sock \
    emacski/tensorflow-serving:latest-devel /bin/bash
    
-curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict
-http://localhost:8501/v1/models/tip_model
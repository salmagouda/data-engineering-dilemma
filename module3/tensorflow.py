import tensorflow as tf
from tensorflow_serving.apis import model_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_log_pb2

def main():
    with tf.python_io.TFRecordWriter("tf_serving_warmup_requests") as writer:
        request = predict_pb2.PredictRequest(
            model_spec=model_pb2.ModelSpec(name="<models>"),
            inputs={"examples": tf.make_tensor_proto(["<tip_model>"])}
        )
    log = prediction_log_pb2.PredictionLog(
        predict_log=prediction_log_pb2.PredictLog(request=request))
    writer.write(log.SerializeToString())

if __name__ == "__main__":
    main()
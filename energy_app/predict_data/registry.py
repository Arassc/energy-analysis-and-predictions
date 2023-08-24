import os
import mlflow
from mlflow.tracking import MlflowClient
import pickle
from tensorflow import keras
from energy_app.utils.parameters import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT,\
                            MODEL_TARGET, LOCAL_REGISTRY_PATH,\
                            MLFLOW_MODEL_NAME

# information https://mlflow.org/docs/latest/tracking.html#tracking-server

def mlflow_run(func):
    def wrapper(*args, **kwargs):
        mlflow.end_run()
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT)
        with mlflow.start_run():
            mlflow.tensorflow.autolog()
            results = func(*args, **kwargs)
        print('mlflow_run auto log done')
        return results
    return wrapper


def save_results(params: dict, metrics: dict, model_name: str):
    """
    Save params & metrics locally on hard drive at
    "{LOCAL_REGISTRY_PATH}/params/{current_timestamp}.pickle"
    "{LOCAL_REGISTRY_PATH}/metrics/{current_timestamp}.pickle"
    - (unit 03 only) if MODEL_TARGET='mlflow', also persist them on mlflow
    """
    if MODEL_TARGET == 'mlflow':
        if params is not None:
            mlflow.log_param(params)
        if metrics is not None:
            mlflow.log_metrics(metrics)
        print('results saved in mlflow')

    else:
        if params is not None:
            params_path = os.path.join(LOCAL_REGISTRY_PATH, 'params', model_name, '.pickle')
            with open(params_path, 'wb') as file:
                pickle.dump(params, file)

        if metrics is not None:
            metrics_path = os.path.join(LOCAL_REGISTRY_PATH, 'metrics', model_name, '.pickle')
            with open(metrics_path, 'wb') as file:
                pickle.dump(metrics, file)

        print('results saved locally')

def save_model(model: keras.Model, model_name: str):
    """ Save trained model locally on hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='mlflow', also persist it on mlflow instead of GCS (for unit 0703 only) --> unit 03 only
    """
    model_path = os.path.join(LOCAL_REGISTRY_PATH, model_name)
    model.save(model_path)

    if MODEL_TARGET == "mlflow":
        mlflow.tensorflow.log_model(model=model,
                        artifact_path="model",
                        registered_model_name=MLFLOW_MODEL_NAME
                        )

#TODO load_model
#TODO mlflow_transion_model

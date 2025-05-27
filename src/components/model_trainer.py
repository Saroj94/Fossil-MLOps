import sys
from typing import Tuple
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score,mean_squared_error
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_numpy_array_data,load_object,save_object
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,RegressionMetricArtifact
from src.entity.estimator import MyModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                       model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config

    def get_model_object_and_report(self, train:np.array, test:np.array)->Tuple[object,object]:
        """
        Method: get_model_object_and_report
        Description: this function takes training & testing data and train on GradientBoostingRegression.
        Output: Returns metric artifact and trained model object
        """
        try:
            logging.info("Splitting the train and test data")
            x_train = train[:, :-1]
            y_train = train[:, -1]
            x_test = test[:, :-1]
            y_test = test[:, -1]

            logging.info("Training GradientBoostingRegressor with specified parameters😊")
            model=GradientBoostingRegressor(
                subsample=self.model_trainer_config.subsample,
                n_estimators=self.model_trainer_config.n_estimetors,
                min_samples_split=self.model_trainer_config.min_samples_split,
                min_samples_leaf=self.model_trainer_config.min_samples_leaf,
                max_features=self.model_trainer_config.max_features,
                max_depth=self.model_trainer_config.max_depth,
                random_state=self.model_trainer_config.random_state,
                learning_rate=self.model_trainer_config.learning_rate
            )
            logging.info("Model Training with x_train and y_train")
            logging.info("Fit the model🤞")
            model.fit(x_train,y_train)
            logging.info("Model Training completed.")

            logging.info("Prediction and Evaluation started.")
            y_pred=model.predict(x_test)
            MSE=mean_squared_error(y_test,y_pred)
            R2score=r2_score(y_test,y_pred)

            logging.info("Creating Regression Report Artifact!!😀")
            metric_artifact=RegressionMetricArtifact(MSE,R2score)
            return model, metric_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        logging.info("The initiate_model_trainer method runs to execute ModelTrainer class")
        try:
            logging.info("Loading the transformed train and test data")
            train_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            logging.info("Data loading is completed")

            logging.info("Training model and create the Accuracy Report🤞")
            trained_model,metric_artifact=self.get_model_object_and_report(train=train_arr, test=test_arr)
            logging.info("Model object and artifact loaded.")

            logging.info("Load Preprocessing Object")
            preprocessing_obj=load_object(self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Preprocessing object is loaded")

            logging.info("Checking r2_squared threshold score")  
            if r2_score(train_arr[:,-1],trained_model.predict(train_arr[:,:-1]))<self.model_trainer_config.expected_score:
                logging.info("The Expected threshold score not meet😔")
                raise Exception("No model found with score above the base score😩")
            logging.info("Saving new model as performace is better than the previous one.")
            my_new_model=MyModel(preprocessing_object=preprocessing_obj,trained_model_object=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path, my_new_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            logging.info("Create and return the ModelTrainerArtifact") 
            model_trainer_artifact=ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path,
                                                        metric_artifact=metric_artifact)
            logging.info("Model trainer artifact created👍")  
            return model_trainer_artifact                  
        except Exception as e:
            raise MyException(e,sys)
        




import sys
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import MyException

class MyModel:
    def __init__(self,preprocessing_object:Pipeline, trained_model_object:object):
        self.preprocessing_object=preprocessing_object
        self.trained_model_object=trained_model_object

    def transform_predict(self,dataframe:pd.DataFrame)-> DataFrame:
        try:
            logging.info("Starting prediction Process.")
            logging.info("Step-1: Applying transformation using pre-trained preprocesing object")
            transformed_features=self.preprocessing_object.transform(dataframe)

            logging.info("Step-2: Perform Prediction on data using pre-trained model")
            prediction=self.trained_model_object.predict(transformed_features)
            logging.info("Transform and Prediction process completed👍")
            return prediction
        except Exception as e:
            logging.error("Error occured in predict method😩")
            raise MyException(e,sys)
        
    def __repr__(self):
        return f"{type(self.preprocessing_object).__name__}()"

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
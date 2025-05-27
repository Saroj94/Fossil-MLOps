import sys
import pandas as pd
from typing import Optional
from src.exception import MyException
from src.logger import logging
from src.constants import TARGET_COLUMN
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact,ModelEvaluationArtifact,ModelEvaluationResponse
from src.utils.main_utils import load_object
from sklearn.metrics import r2_score,mean_squared_error
from src.entity.s3_estimator import FossilEstimator
from dataclasses import dataclass
    
class ModelEvaluation:
    def __init__(self,model_eval_config:ModelEvaluationConfig, 
                 data_ingestion_artifact:DataIngestionArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def get_best_model(self)->Optional[FossilEstimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path=self.model_eval_config.s3_model_key_path
            fossil_estimator=FossilEstimator(bucket_name=bucket_name,
                                             model_path=model_path)
            if fossil_estimator.is_model_present(model_path=model_path):
                return fossil_estimator
            return None
        except Exception as e:
            raise MyException(e,sys)
        
    def evaluate_model(self)->ModelEvaluationResponse:
        try:
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            x,y=test_df.drop(columns=[TARGET_COLUMN],axis=1),test_df[TARGET_COLUMN]
            
            trained_model= load_object(file_path=self.model_trainer_artifact.trained_model_file)
            trained_model_r2_square=self.model_trainer_artifact.metric_artifact.r2_squared
            logging.info(f"R2 Squared score: {trained_model_r2_square}")
            best_model_r2_square=None
            best_model=self.get_best_model()
            if best_model is not None:
                y_pred_best_model=best_model.predict(x)
                best_model_score=r2_score(y_pred_best_model,y)

            temp_best_model_score=0 if best_model_r2_square is None else best_model_r2_square
            result=ModelEvaluationResponse(trained_model_r2_squared=trained_model_r2_square,
                                           best_model_r2_squared_score=best_model_r2_square,
                                           is_model_accepted=trained_model_r2_square>temp_best_model_score,
                                           difference=trained_model_r2_square-temp_best_model_score)
            return result
        except Exception as e:
            raise MyException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            logging.info("Initialized Model Evaluation Component.")
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(
            is_model_accepted=evaluate_model_response.is_model_accepted,
            s3_model_path=s3_model_path,
            trained_model_path=self.model_trainer_artifact.trained_model_file,
            changed_accuracy=evaluate_model_response.difference)

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys)

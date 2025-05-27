"""Training the model with the ingested data"""

import os
import sys
from src.exception import MyException
from src.logger import logging

##For data ingestion pipeline setup
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngestion

##dependencies for data validation 
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact
from src.components.data_validation import DataValidation

##dependencies for data transformation
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact
from src.components.data_transformation import DataTransformation

##dependencies for model training
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact
from src.components.model_trainer import ModelTrainer

##dependencies for model evaluation
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelEvaluationArtifact
from src.components.model_evaluation import ModelEvaluation

##dependencies for model pusher
from src.entity.config_entity import ModelPusherConfig
from src.entity.artifact_entity import ModelPusherArtifact
from src.components.model_pusher import ModelPusher


class TrainPipeline:
    """Initialze data ingestion configuration """
    def __init__(self):
        """initialise the Data ingestion configuration because it has 
        required information about the data, it's naming and its location even it's artifacts name and folder"""
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig() ##i spent a lot of time on this to debug due to my small mistake, cause i wrote DataValidationArtifact instead.
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        self.model_eval_config=ModelEvaluationConfig()
        self.model_pusher_config=ModelPusherConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingested()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        """This Method is responsible for validating the data."""
        logging.info("Data Validation started")
        try:
            logging.info("To initiate data validation first access ingested data from data ingestion folder")
            #read the data from ingested data of ingested folder
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Data validation stopped")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def start_data_transformation(self,data_ingestion_artifact=DataIngestionArtifact,
                                  data_validation_artifact=DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                   data_validation_artifact=data_validation_artifact,
                                                   data_transformation_config=DataTransformationConfig)
            data_transformation_artifact=data_transformation.initiate_data_transformtion()
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def start_model_trainer(self,data_tranformation_artifact=DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer=ModelTrainer(data_transformation_artifact=data_tranformation_artifact,
                                       model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def start_model_evaluation(self, data_ingestion_artifact=DataIngestionArtifact,
                               model_trainer_artifact=ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation=ModelEvaluation(model_eval_config=self.model_eval_config,
                                             data_ingestion_artifact=data_ingestion_artifact,
                                             model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def start_model_pusher(self,model_evaluation_artifact=ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            model_pusher=ModelPusher(model_pusher_config=self.model_pusher_config,
                                     model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact=model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys)
    
    def run_pipeline(self,)->None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_tranformation_artifact=data_transformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                  model_trainer_artifact=model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                return None
            else:
                model_pusher_artifact=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
        except Exception as e:
            raise MyException(e,sys)
        
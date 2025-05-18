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


class TrainPipeline:
    """Initialze data ingestion configuration """
    def __init__(self):
        """initialise the Data ingestion configuration because it has 
        required information about the data, it's naming and its location even it's artifacts name and folder"""
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig() ##i spent a lot of time on this to debug due to my small mistake

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
    
    def run_pipeline(self,)->None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise MyException(e,sys)
        
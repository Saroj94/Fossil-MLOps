import os
import sys
from src.exception import MyException
from src.logger import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.fetch_data import FetchData

class DataIngestion:
    """Initialize the Data Ingestion Configuration to Ingest the data"""
    def __init__(self, data_ingestion_config: DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
    
    """Export the data into Feature Store Folder"""
    def export_data(self)->DataFrame:
        try:
            logging.info("Starting Exporting data from mongodb")
            data=FetchData()
            df=data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of the data {df.shape}")
            ##put these freshly imported data into feature_store_file_path folder
            logging.info("Storing imported data into feature_store_file_path folder")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path) ##directory name
            os.makedirs(dir_path, exist_ok=True) ## make directory from above mentioned path
            logging.info(f"Saving exported data into feature store file path folder")
            df.to_csv(feature_store_file_path, index=False, header=True)
            return df
        
        except Exception as e:
            raise MyException(e,sys)

    """Split data into train and test data"""
    def train_test_split(self, data: DataFrame)->None:
        try:
            train_set,test_set=train_test_split(data, test_size=self.data_ingestion_config.train_test_split_size)
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path) ##
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f" Store train and test data into training folder")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info(f"Data exported completed")
        except Exception as e:
            raise MyException(e,sys)

    """Initiate the data ingestion"""
    def initiate_data_ingested(self)->DataIngestionArtifact:
        """
        Method: Data ingestion started.
        Basically, this method initiates the data ingestion method that perform 3 steps in pipeline for exporting data as follows:
            1. Export Data from mongodb
            2. Train Test Split
            3. Initiate data ingestion 
        """
        try:
            ##export data
            data=self.export_data()
            ##split data into train test set
            self.train_test_split(data)
            ##initiate the data ingestion
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, 
                                                          test_file_path=self.data_ingestion_config.test_file_path)
            logging.info("Initiate data ingestion")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)




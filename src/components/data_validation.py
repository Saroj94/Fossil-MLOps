import os
import sys
import json
import pandas as pd
from pandas import DataFrame
from src.logger import logging
from src.exception import MyException
from src.utils.main_utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.constants import SCHEMA_FILE_PATH

##data validation class
class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig,file_path=SCHEMA_FILE_PATH):
        """Initialize the objects for ingestion data, validation config and yaml file"""
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(file_path)
            logging.info("Returning the data validation artifact.")
        except Exception as e:
            raise MyException(e, sys)
        
    ##validate number of columns present in the dataset
    def validate_number_of_columns(self, dataframe: DataFrame)->bool:
        """This method returns the boolean outputs like True or False"""
        logging.info("Comparing the columns of imported data from database and columns of yaml file")
        try:
            ##Check and compare the len of imported dataframe column and column of yaml schema
            status=len(dataframe.columns)==len(self.schema_config["columns"])
            logging.info(f"Is required column present: {status}")
            return status
        except Exception as e:
            raise MyException(e,sys)
        
    ##check column data type
    def validate_feature_datatype(self, df: DataFrame)->bool:
        try:
            dataframe_cols=df.columns
            missing_numerical_columns=[]
            missing_categorical_columns=[]
            #numerical column checks
            for column in self.schema_config['numerical_columns']:
                if column not in dataframe_cols:
                    missing_numerical_columns.append(column)

            #categorical column checks
            for column in self.schema_config["categorical_columns"]:
                if column not in dataframe_cols:
                    missing_categorical_columns.append(column)
            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_data(file)->DataFrame:
        try:
            return pd.read_csv(file)
        except Exception as e:
            raise MyException(e,sys)
        

    ##start data validation
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info("Initiate data validation")
            validation_error_message=""
            ##access data stored in Artifact folder when data ingestion pipeline executed 
            train_df,test_df= (DataValidation.read_data(self.data_ingestion_artifact.trained_file_path),
                        DataValidation.read_data(self.data_ingestion_artifact.test_file_path))
            
            ##checking len of the columns of dataframe for train/test
            train_column_len_status=self.validate_number_of_columns(train_df)
            test_column_len_status=self.validate_number_of_columns(test_df)

            ##append message based on status
            if not train_column_len_status:
                validation_error_message +="Columns are missing in training set of dataframe."
            else:
                logging.info(f"All required columns are present in the training set of dataframe: {train_column_len_status}")

            if not test_column_len_status:
                logging.info(f"All required columns are present in the test set of dataframe: {test_column_len_status}")
            else:
                logging.info(f"All required columns are present in test set of test set of dataframe:{test_column_len_status}")

            ##checking datatype of train/test dataframe
            train_datatype_status=self.validate_feature_datatype(train_df)
            test_datatype_status=self.validate_feature_datatype(test_df)

            ##validation 
            if not train_datatype_status:
                validation_error_message +="Columns are missing in training set of dataframe based on Data types."
            else:
                logging.info(f"All required columns are present in the training set of Dataframe: {train_datatype_status}")

            if not test_datatype_status:
                validation_error_message +="Columns are missing in training set of dataframe based on data types."
            else:
                logging.info(f"All required columns are present in test set of dataframe: {test_datatype_status}")

            ##store the message as nothing/empty/message either there is no misisng columns or missing columns
            validation_status = len(validation_error_message) == 0

            ##make report for data validation
            data_validation_artifact=DataValidationArtifact(validation_status=validation_status,
                                                            message=validation_error_message,
                                                            validation_report_file_path=self.data_validation_config.validation_report_file_path)
                                                                        
            ##path of the directory for the data validation report file should store
            report_path_dir=os.path.dirname(self.data_validation_config.validation_report_file_path)

            #create the folder 
            os.makedirs(report_path_dir, exist_ok=True)

            ##save the report file in JSON format
            validation_report={
                "Validation Status": validation_status,
                "Message": validation_error_message.strip()}

            ##open the report and format into a JSON file format
            with open(self.data_validation_config.validation_report_file_path,'w') as report_file:
                json.dump(validation_report,report_file, indent=4)
            
            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys)




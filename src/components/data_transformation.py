import sys
import pandas as pd
import numpy as np
from src.exception import MyException
from src.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact,DataIngestionArtifact
from src.utils.main_utils import save_object,save_numpy_array_data,read_yaml_file

##data transformation class 
class DataTransformation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                    data_validation_artifact:DataValidationArtifact,
                    data_transformation_config:DataTransformationConfig,
                    file=SCHEMA_FILE_PATH):
        try:   
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
            self.schema_config=read_yaml_file(file)
        except Exception as e:
            raise MyException(e,sys)
    @staticmethod   
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
        
    ##transformation method
    def get_data_transformer_object(self)->Pipeline:
        logging.info("Entered into the get-data-transformer-object method of DataTransformer class")
        try:
            "Initialize all the transformer"
            scaling_transformer=StandardScaler()
            categorical_transformer=OrdinalEncoder()

            "Load all schemas for configuration"
            numerical_features=self.schema_config['numerical_columns']
            categorical_features=self.schema_config['categorical_columns']

            "Creating preprocessor pipeline"
            preprocessor=ColumnTransformer(transformers=[("scaling",scaling_transformer,numerical_features),
                                                         ("Encoding",categorical_transformer,categorical_features)],remainder='passthrough')
            
            logging.info("Final Pipeline Ready!!")
            ##combine all the pipeline into one
            final_pipeline=Pipeline(steps=[("Preprocessing",preprocessor)])
            return final_pipeline
        
        except Exception as e:
            raise MyException(e,sys)

    def drop_column(self, df):
        logging.info("Drop the column-id from the data")
        drop_column=self.schema_config['drop_column']
        logging.info(f"Drop column name: {drop_column}")
        logging.info(f"Columns present in the data:{df.columns.to_list()}")
        if drop_column in df.columns:
            df=df.drop(drop_column, axis=1)
        else:
            logging.info(f"Column {drop_column} not found in the DataFrame, skipping drop.")
        return df
    
    def initiate_data_transformtion(self)->DataTransformationArtifact:
        "Initaiting the data transformation"
        try:
            logging.info("Data Transformation started")
            ##condition check first
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            "Loading the Data to perform data transformation"
            logging.info("Data Loading started............!!!")
            train_df=self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df=self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info("Data loading completed")

            logging.info(f"Train DataFrame shape: {train_df.shape}")
            logging.info(f"Test DataFrame shape: {test_df.shape}")
            logging.info(f"Train DataFrame columns: {train_df.columns.to_list()}")
            logging.info(f"Test DataFrame columns: {test_df.columns.to_list()}")
            logging.info(f"Train DataFrame head: {train_df.head()}")
            logging.info(f"Test DataFrame head: {test_df.head()}")

            logging.info("Create independent and dependent feature by droping response column")
            train_input_feature_df= train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target_input_df=train_df[TARGET_COLUMN]

            test_input_feature_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target_input_df=test_df[TARGET_COLUMN]
            logging.info("Independent and Dependent feature")

            logging.info(f"Columns present in the Train Dataset:{train_input_feature_df.columns.to_list()}")
            logging.info(f"Columns present in the Test Dataset:{test_input_feature_df.columns.to_list()}")
            "Apply transformation on data"
            # logging.info("Applying custom Transformation on train and test data.")
            # input_feature_train_df=self.drop_column(train_input_feature_df)
            # input_feature_test_df=self.drop_column(test_input_feature_df)
            # logging.info("Custom Transformation on independent features of train and test completed.")

            "Starting the data transformation"
            logging.info("Initializing the Transformer.")
            preprocess=self.get_data_transformer_object()

            logging.info("Fit and Transform train data.")
            input_feature_train_arr=preprocess.fit_transform(train_input_feature_df)
        
            logging.info("Fit and Transform to test data.")
            input_feature_test_arr=preprocess.transform(test_input_feature_df)

            logging.info("Combine Target column and Independent Columns together.")
            train_arr=np.c_[input_feature_train_arr,np.array(train_target_input_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(test_target_input_df)]
            logging.info("Array combination is completed.")

            "Save objects of transformation."
            logging.info("Saving preprocessing transformation model as object inside the t.")
            save_object(self.data_transformation_config.transformed_object_file_path,preprocess)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            logging.info("Saving transformed file and object is successfully completed.")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise MyException(e,sys)
    



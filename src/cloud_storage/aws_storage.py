import os,sys
import boto3
import pickle
from io import StringIO
from typing import Union,List
from src.exception import MyException
from src.logger import logging
from src.configuration.aws_connection import S3client
from pandas import DataFrame,read_csv
from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientError

"AWS Simple Storage Service(S3): Set up the S3 bucket to store model and access it from anywhere."

class SimpleStorageService:
    """A class for interacting with AWS s3 bucket(storage), providing methods(way) for file mangement, 
    data uploads, and data retrieval from S3 bucket.
    """
    def __init__(self):
        """
        Initialiazes the SimpleStorageServices(s3) instances with S3 resources and client from the S3Client
        class.
        """
        s3_client=S3client()
        self.s3_resource=s3_client.s3_resource
        self.s3_client=s3_client.s3_client

    def get_bucket(self, bucket_name:str) -> Bucket:
        """
        Fetch the s3 bucket object based on the provided bucket name. 
        """
        logging.info("Enter the get_bucket method of SimpleStorageService class to retrieve s3 bucket🪣😆")
        try:
            bucket=self.s3_resource.Bucket(bucket_name)
            logging.info("Exited from get_bucket method.")
            return bucket
        except Exception as e:
            raise MyException(e,sys)


    def s3_key_path_checker(self,bucket_name, s3_key)->bool:
        """Checks if specified s3 key path is available in the specified bucket.
        Args:
            bucket_name (str): Name of the S3 bucket.
            s3_key (str): Key path of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            logging.info("Checking the presence of file in S3 bucket")
            bucket=self.get_bucket(bucket_name)
            file_object=[file for file in bucket.objects.filter(Prefix=s3_key)]
            return len(file_object)>0
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Reads the specified S3 object with optional decoding and formatting.
        """
        # logging.info("Entered the read_object method of SimpleStorageService class")
        try:
            # Read and decode the object content if decode=True
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode else object_name.get()["Body"].read()
            )
            # Convert to StringIO if make_readable=True
            conv_func = lambda: StringIO(func()) if make_readable else func()
            # logging.info("Exited the read_object method of SimpleStorageService class")
            return conv_func()
        except Exception as e:
            raise MyException(e, sys)
    
    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        """
        Retrieves the file object(s) from the specified bucket based on the filename.
        """
        logging.info("Entered the get_file_object method of SimpleStorageService class")
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(file_objects)
            logging.info("Exited the get_file_object method of SimpleStorageService class")
            return file_objs
        except Exception as e:
            raise MyException(e, sys)
        
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        """
        Loads a serialized model from the specified S3 bucket.
        """
        try:
            model_file = model_dir + "/" + model_name if model_dir else model_name
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = pickle.loads(model_obj)
            logging.info("Production model loaded from S3 bucket.")
            return model
        except Exception as e:
            raise MyException(e, sys)
        
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a folder in the specified S3 bucket.
        """
        logging.info("Entered the create_folder method of SimpleStorageService class")
        try:
            # Check if folder exists by attempting to load it
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            # If folder does not exist, create it
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            logging.info("Exited the create_folder method of SimpleStorageService class")
    
    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        """
        Uploads a local file to the specified S3 bucket with an optional file deletion.
        """
        logging.info("Entered the upload_file method of SimpleStorageService class")
        try:
            logging.info(f"Uploading {from_filename} to {to_filename} in {bucket_name}")
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            logging.info(f"Uploaded {from_filename} to {to_filename} in {bucket_name}")
            
            # Delete the local file if remove is True
            if remove:
                os.remove(from_filename)
                logging.info(f"Removed local file {from_filename} after upload")
            logging.info("Exited the upload_file method of SimpleStorageService class")
        except Exception as e:
            raise MyException(e, sys)
        
    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        """
        Uploads a DataFrame as a CSV file to the specified S3 bucket.
        """
        logging.info("Entered the upload_df_as_csv method of SimpleStorageService class")
        try:
            # Save DataFrame to CSV locally and then upload it
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
            logging.info("Exited the upload_df_as_csv method of SimpleStorageService class")
        except Exception as e:
            raise MyException(e, sys)
        
    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Converts an S3 object to a DataFrame.
        """
        logging.info("Entered the get_df_from_object method of SimpleStorageService class")
        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logging.info("Exited the get_df_from_object method of SimpleStorageService class")
            return df
        except Exception as e:
            raise MyException(e, sys)
    
    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Reads a CSV file from the specified S3 bucket and converts it to a DataFrame.
        """
        logging.info("Entered the read_csv method of SimpleStorageService class")
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            logging.info("Exited the read_csv method of SimpleStorageService class")
            return df
        except Exception as e:
            raise MyException(e, sys)
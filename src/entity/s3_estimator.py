import sys
from src.exception import MyException
from pandas import DataFrame
from src.entity.estimator import MyModel
from src.cloud_storage.aws_storage import SimpleStorageService


class FossilEstimator:
    "This class save and retrieve model from s3 bucket and to do prediction."
    def __init__(self, bucket_name,model_path,):
        """
        bucket_name: Name of the bucket,
        model_path: Location of the model in aws bucket.
        """
        self.bucket_name=bucket_name
        self.model_path=model_path
        self.s3=SimpleStorageService()
        self.loaded_model:MyModel=None

    def is_model_present(self,model_path):
        try:
            return self.s3.s3_key_path_checker(bucket_name=self.bucket_name,s3_key=model_path)
        except Exception as e:
            print(e) 
            return False
        
    def load_model(self,)->MyModel:
        "Load the model from model path"
        return self.s3.load_model(self.model_path,bucket_name=self.bucket_name)
    
    def save_model(self,from_file,remove:bool=False)->None:
        """
        Save the model to the model_path
        from_file: Your local system model path
        remove: By default it is false that mean 
                you will have your model locally available in your system folder
        """
        try:
            self.s3.upload_file(from_file,
                                to_filename=self.model_path,
                                bucket_name=self.bucket_name,
                                remove=remove)
        except Exception as e:
            raise MyException(e,sys)
        
    def predict(self,dataframe:DataFrame):
        "dataframe"
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.transform_predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e,sys)
         
        
    
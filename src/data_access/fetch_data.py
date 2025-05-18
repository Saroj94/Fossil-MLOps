"""
Once the mongodb client connection is set up. we have to fetch the data from the database.
"""
import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.exception import MyException
from src.configuration.mongo_db_connection import MongoDBClient
from src.logger import logging
from src.constants import DATABASE_NAME

class FetchData:
    """Class that export the Mongodb records into a pandas dataframe"""

    def __init__(self)->None:
        try:
            self.mongoclient=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str]=None)-> pd.DataFrame:
        """fetch the records from mogodb database into pandas dataframe

        Returns:
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            if database_name is None:
                collection = self.mongoclient.database[collection_name]
            else:
                collection = self.mongoclient.client[database_name][collection_name]
            
            ##convert records into dataframe
            logging.info("Start feaching data from mongodb collection")
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns="_id", axis=1)
            df.replace({"na": np.nan}, inplace=True)
            logging.info("Data fetched from mongodb")
            return df
            
        except Exception as e:
            raise MyException(e,sys)
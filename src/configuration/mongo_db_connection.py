##Establish the connection with database through connection string
import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME,MONGODB_URL


# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca=certifi.where()

class MongoDBClient:
    """
    Mongodbclient class is responsible to establish the mongodb

    Attributes: client/ it is the shared variable in entire class. 

    Method: __init__(database_name: str)
    """
    ##static variable
    client=None ## shared the instance accross class

    def __init__(self, database_name: str = DATABASE_NAME)->None:
        try:
            """First it checks the client whether it is none or contain value,Then if mongodb url is empty raise the exception."""
            if MongoDBClient.client is None: ##check initially the client is none or not
                mongodb_url=MONGODB_URL ##fetch the mongodb url to establish the client
                if mongodb_url is None:
                    raise Exception(f'Connection environment variable {MONGODB_URL} is not set.')
                ##establish the new mongodb client connection
                MongoDBClient.client=pymongo.MongoClient(mongodb_url,tlsCAFile=ca) 

            ##if exist then Use the mongoclient  for this instances
            self.client=MongoDBClient.client
            self.database=self.client[database_name] ##connecting with database
            self.database_name=database_name
            print(f"MongoDB connection is successful ✅, {self.database}")
        except Exception as e:
            raise MyException(e, sys)

        

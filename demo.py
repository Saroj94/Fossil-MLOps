import sys
from src.exception import MyException
from src.logger import logging
from src.constants import MONGODB_URL

from src.data_access.fetch_data import FetchData
from src.constants import COLLECTION_NAME,DATABASE_NAME
from src.configuration.mongo_db_connection import MongoDBClient
from src.pipline.training_pipeline import TrainPipeline



# logging.debug("This is a debug message.")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")
# try:
#     x=10/0
# except Exception as e:
#     logging.info(e)
#     raise MyException(e,sys)

# print(MONGODB_URL)
# mg=MongoDBClient()
# print(mg)
# ft=FetchData()
# tab=ft.export_collection_as_dataframe(collection_name=COLLECTION_NAME,database_name=DATABASE_NAME)
# print(tab.head())

tb=TrainPipeline()
print(tb.run_pipeline())
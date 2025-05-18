import os
from datetime import datetime,date
from dotenv import load_dotenv
load_dotenv()

##Logging constants
LOGS="logs"
LOG_FILE_FORMAT=f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'
LOG_SIZE=5*1024*1024
BACKUPCOUNT=3

##establish connection
MONGODB_URL=os.getenv("URI")
DATABASE_NAME="Fossil"
COLLECTION_NAME="Fossil_tab"

##pipeline variables
PIIPELINE_NAME: str =""
FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")

##Arrtifact name
ARTIFACT_DIR: str = "artifact"

"""
Data Ingestion constant names over entire project
"""
DATA_INGESTION_COLLECTION_NAME: str ="Fossil_tab"
DATA_INGESTION_DIR_NAME: str ="Data Ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="Ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: str = 0.20

"""Data Validation constants"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME:str = "report.yaml"



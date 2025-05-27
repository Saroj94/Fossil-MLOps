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
MONGODB_URL=os.getenv("URL")
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

"Data Ingestion constant names over entire project"
DATA_INGESTION_COLLECTION_NAME: str ="Fossil_tab"
DATA_INGESTION_DIR_NAME: str ="Data Ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="Ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: str = 0.20

"Data Validation constants"
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME:str = "report.yaml"

"Data Transformation constants"
TARGET_COLUMN="age"
CURRENT_YEAR=date.today().year
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
DATA_TRANSFORMATION_DIR_NAME: str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str="transformed_object"

"Model Training constants"
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.9
N_ESTIMATORS:int = 400
SUBSAMPLE:float = 1.0
MIN_SAMPLES_SPLIT:int = 10
MIN_SAMPLES_LEAF:int = 2
MAX_FEATURES:str = 'sqrt'
MAX_DEPTH:int = 4
LEARNING_RATE:float = 0.05
RANDOM_STATE:int = 42
MODEL_FILE_NAME:str = "model.pkl"


"AWS credentials"
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID=os.getenv("AWS_SECRET_ACCESS_KEY_ID")
AWS_REGION=os.getenv("AWS_REGION")


"Model Evaluation Related Constants"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float =0.2
MODEL_BUCKET_NAME = "fossilproject"
MODEL_PUSHER_S3_KEY="model-registry"

"App Host constants"
APP_HOST="localhost"
APP_PORT=5000




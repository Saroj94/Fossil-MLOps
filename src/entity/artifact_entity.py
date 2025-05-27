"""In artifact section we expect only the outputs in a classes format"""
from dataclasses import dataclass

##data ingestion artifact
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str


##data validation artifact
@dataclass
class DataValidationArtifact:
    validation_status:bool
    message:str
    validation_report_file_path:str

##data transformation 
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class RegressionMetricArtifact:
    mean_squared_error: float
    r2_squared:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file:str
    metric_artifact:RegressionMetricArtifact


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    s3_model_path:str
    trained_model_path:str

@dataclass
class ModelEvaluationResponse:
    trained_model_r2_squared: float
    best_model_r2_squared_score: float
    is_model_accepted:bool
    difference:float

@dataclass
class ModelPusherArtifact:
    bucket_name:str
    s3_model_path:str

    


import sys
from src.entity.config_entity import FossilPredictionConfig
from src.entity.s3_estimator import FossilEstimator
from src.exception import MyException
from src.logger import logging
from pandas import DataFrame

class FossilPrediction:
    def __init__(self,
                uranium_lead_ratio,        
                carbon_14_ratio,           
                radioactive_decay_series,  
                stratigraphic_layer_depth, 
                geological_period,         
                paleomagnetic_data,        
                inclusion_of_other_fossils,
                isotopic_composition,      
                surrounding_rock_type,     
                stratigraphic_position,    
                fossil_size,               
                fossil_weight):
        try:
                self.uranium_lead_ratio= uranium_lead_ratio        
                self.carbon_14_ratio =  carbon_14_ratio         
                self.radioactive_decay_series =  radioactive_decay_series
                self.stratigraphic_layer_depth = stratigraphic_layer_depth
                self.geological_period=  geological_period        
                self.paleomagnetic_data =  paleomagnetic_data      
                self.inclusion_of_other_fossils= inclusion_of_other_fossils
                self.isotopic_composition =  isotopic_composition    
                self.surrounding_rock_type =  surrounding_rock_type   
                self.stratigraphic_position =  stratigraphic_position  
                self.fossil_size= fossil_size               
                self.fossil_weight= fossil_weight
        except Exception as e:
            raise MyException(e,sys)
        
    def get_fossil_data_in_dict(self):
             try:
                input_data={
                "uranium_lead_ratio":[self.uranium_lead_ratio],
                "carbon_14_ratio":[self.carbon_14_ratio],
                "radioactive_decay_series":[self.radioactive_decay_series],
                "stratigraphic_layer_depth":[self.stratigraphic_layer_depth],
                "geological_period":[self.geological_period],
                "paleomagnetic_data":[self.paleomagnetic_data],
                "inclusion_of_other_fossils":[self.inclusion_of_other_fossils],
                "isotopic_composition":[self.isotopic_composition],
                "surrounding_rock_type":[self.surrounding_rock_type],
                "stratigraphic_position":[self.stratigraphic_position],
                "fossil_size":[self.fossil_size],
                "fossil_weight":[self.fossil_weight]
                }
                return input_data
             except Exception as e:
                  raise MyException(e,sys)
        
    def get_fossil_input_dataframe(self)->DataFrame:
             "This function returns a dataframe from fossil data class input."
             try:
                  fossil_input_dict=self.get_fossil_data_in_dict()
                  return DataFrame(fossil_input_dict)
             except Exception as e:
                  raise MyException(e,sys)
             
            
class FossilAgeRegression:
    def __init__(self,prediction_pipeline_config:FossilPredictionConfig=FossilPredictionConfig(),)->None:
          try:
               self.predict_pipeline_config=prediction_pipeline_config
          except Exception as e:
               raise MyException(e,sys)
          
    def predict(self,dataframe)->str:
         try:
              model=FossilEstimator(
                   bucket_name=self.predict_pipeline_config.model_bucket_name,
                   model_path=self.predict_pipeline_config.model_file_path,
              )
              result=model.predict(dataframe)
              return result
         except Exception as e:
              raise MyException(e,sys)
          
             
        

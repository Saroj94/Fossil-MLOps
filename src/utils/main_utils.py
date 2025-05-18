import os
import sys
import numpy as np
import dill
import yaml
from pandas import DataFrame
from src.logger import logging
from src.exception import MyException

##method to read yaml file
def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise MyException(e,sys)
    
##write on yaml file 
def write_yaml_file(file_path: str, content: object, replace: bool=False)-> None:
    try:
        """This avoids issues with overwriting files that might be locked, 
        corrupted, or contain old content"""
        if replace:
            """This block of code is used to safely delete a file from the system if it exists"""
            if os.path.exists(file_path): #This checks whether a file (or directory) exists at the given path stored in file_path
                os.remove(file_path) #If the file does exist, this line deletes it
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise MyException(e,sys)
    
##load object:
def load_object(file_path: str)->object:
    """This method is responsible for loading the data. so object could be any thing like model,dataset, file etc."""
    try:
        with open(file_path,'rb') as file_obj:
            obj=dill.load(file_obj)
            return obj        
    except Exception as e:
        raise MyException(e,sys)
    
##save as numpy array: save data as numpy array
def save_numpy_array_data(file_path: str, array:np.array):
    try:
        ##create directory path
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        ##open file in read byte mode and save as numpy array
        with open(file_path, 'rb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MyException(e,sys)
    
##load the numpy array
def load_numpy_array_data(file_path: str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException(e,sys)
    

##save the object
def save_object(file_path:str, obj:object)->None:
    logging.info("Saving object is started")
    try:
        dir_path=os.path.dirname(file_path) #file path name
        os.makedirs(dir_path,exist_ok=True) #create directory with file path name
        with open(file_path,'w') as file_obj:
            dill.dump(file_obj,obj)
        logging.info("Object is save in the folder")
    except Exception as e:
        raise MyException(e,sys)

import pandas as pd
import numpy  as np
import os,sys
from pathlib import Path

import yaml # 
import json
import joblib
import pickle

# from box import ConfigBox

from typing import Any

import base64

class Predict:
    def __init__(self,config_path:str):
        self.config = self.read_yaml(config_path)
    
    def read_yaml(self,config_path):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def load_pickle(self,file_path):
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    
    def load_joblib(self,file_path):
        return joblib.load(file_path)
    
    def predict(self,data):
        model_path, transform_path = self.config['model_path'], self.config['preprocessor_path']

        # model = self.load_joblib(model_path)
        # transform_obj = self.load_joblib(transform_path)
        model = joblib.load(model_path)
        transform_obj = joblib.load(transform_path)

        data_transform = transform_obj.transform(data)

        predict = model.predict(data_transform)
        
        # target encode
        target_encode = ['Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II','Obesity_Type_I','Obesity_Type_II','Obesity_Type_III']

        return target_encode[predict]
        

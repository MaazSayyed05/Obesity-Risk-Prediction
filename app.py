
import streamlit as st
import pandas as pd
import numpy as np
import os,sys
from pathlib import Path
import json
import pickle
import yaml
import joblib

# from box import ConfigBox

from typing import Any

import base64

from src.obesity_risk_pred.components.predict import Predict
from src.obesity_risk_pred.utils.common import read_yaml,load_pickle,load_json

# from src.obesity_risk_pred.utils import load_json
# from src.obesity_risk_pred.main.Training import predict

# Set title and introduction text
st.title("Obesity Risk Prediction")
st.write("""
Obesity is a significant health issue that increases the risk of several chronic diseases, including diabetes, heart disease, and cancer. 
This tool helps assess the risk of obesity based on various lifestyle and personal health factors.
Please fill in the details below to get a risk prediction.
""")

# Sidebar inputs for user details
st.sidebar.header("User Details")
username = st.sidebar.text_input("Enter User Name")
user_id = st.sidebar.text_input("Enter User ID")
mode = st.sidebar.selectbox("Select Mode", ["Mode 1", "Mode 2", "Mode 3"])

# Main feature inputs
st.subheader("Enter Your Details")

#     "Gender": "object",
    # "Age": "float64",
    # "Height": "float64",
    # "Weight": "float64",
    # "family_history_with_overweight": "object",
    # "FAVC": "object",
    # "FCVC": "float64",
    # "NCP": "float64",
    # "CAEC": "object",
    # "SMOKE": "object",
    # "CH2O": "float64",
    # "SCC": "object",
    # "FAF": "float64",
    # "TUE": "float64",
    # "CALC": "object",
    # "MTRANS": "object",

data = [0]*16
data[0] = st.selectbox('Gender',['Male','Female'])
data[1] = st.number_input('Age', min_value=0, max_value=100)
data[2] = st.number_input('Height(in cms)', min_value=0, max_value=250)
data[3] = st.number_input('Weight(in kgs)', min_value=0, max_value=500)
data[4] = st.selectbox('Family History with Overweight',['yes','no'])
data[5] = st.selectbox('FAVC',['yes','no'])
data[6] = st.number_input('FCVC', min_value=0.0, max_value=3.0)
data[7] = st.number_input('NCP', min_value=0.0, max_value=3.0)
data[8] = st.selectbox('CAEC',['no','Sometimes','Frequently','Always'])
data[9] = st.selectbox('Smoke',['yes','no'])
data[10] = st.number_input('CH2O (Water Intake)', min_value=0.0, max_value=3.0)
data[11] = st.selectbox('SCC',['yes','no'])
data[12] = st.number_input('FAF', min_value=0.0, max_value=3.0)
data[13] = st.number_input('TUE', min_value=0.0, max_value=3.0)
data[14] = st.selectbox('CALC',['no','Sometimes','Frequently','Always'])
data[15] = st.selectbox('Mode of Transport',['Public_Transportation','Automobile','Motorbike','Bike','Walking']) 

# Save result as pd DataFrame
# os.chdir('../../')
schema = load_json('schema.json')

print(schema.keys())

# data = np.array(data).reshape(1,16)
# data = pd.DataFrame(data)
# data.columns = list(schema.keys())[:-1]

df_data=  {}
for i,col in enumerate(schema.keys()):
    if col != 'NObeyesdad':
        df_data[col] = [data[i]]

# data_df = np.array(df_data).reshape(1,16)
st.write(df_data)
df = pd.DataFrame(df_data)
st.table(df)

if st.button('Predict'):

    if not user_id:
        st.warning("Please enter  User ID")
    
    elif not username:
        st.warning("Please enter  User Name")
    
    elif  any(val == '' or val is None for val in data):
        st.warning("Please fill all the required fields")
    
    else:
        # predicted = predict(df)
        # config = read_yaml('config\config.yaml')
        # model_path, transform_path = config['model_path'], config['preprocessor_path']

        # model = load_joblib(model_path)
        # transform_obj = load_joblib(transform_path)

        # data_transform = transform_obj.transform(data)
        config_path = 'config/config.yaml'
        pred_obj = Predict(config_path)
        predict = pred_obj.predict(data)

        # pred_obj = Training(config_path)
        # predict = pred_obj.predict(data)
        
        # target encode
        # target_encode = ['Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II','Obesity_Type_I','Obesity_Type_II','Obesity_Type_III']

        # prediction_result = target_encode[predict]

        st.markdown(f"### Prediction Result: **{predict}**")
        st.success("Prediction Successful")
        st.balloons()


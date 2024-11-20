
import pandas as pd
import numpy  as np
import os,sys
from pathlib import Path

from src.obesity_risk_pred.utils import *


from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.model_selection import  train_test_split
from sklearn.ensemble import  RandomForestClassifier
from sklearn.metrics import  confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
from sklearn.impute import  SimpleImputer
from sklearn.compose import  ColumnTransformer
from sklearn.pipeline import  Pipeline

class Training:
    def __init__(self,config_path:str):
        pass
        self.config = read_yaml(config_path)

    def transform(self):
        # Load data
        data = pd.read_csv(Path(self.config.data_path))

        data = data.drop(['id'],axis=1)
        
        # Save Schema of 
        save_json(Path(self.config.schema_path),data.dtypes.apply(lambda x: x.name).to_dict())

        # num_cols and cat_cols
        num_cols = [col for col in data.columns if data[col].dtype != 'object']
        cat_cols = [col for col in data.columns if data[col].dtype == 'object']
        cat_cols.remove('NObeyesdad')
        
        # cat_encode
        cat_encode = [
        
            ['Male','Female'],
            ['no','yes'], ## 1
            ['no','yes'], ## 2
            ['no','Sometimes','Frequently','Always'], ## 3
            ['no','yes'], ## 4
            ['no','yes'], ## 5
            ['no','Sometimes','Frequently','Always'], ## 6
            ['Walking','Bike','Motorbike','Automobile','Public_Transportation'], ## 7
            # ['Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II','Obesity_Type_I','Obesity_Type_II','Obesity_Type_III'], ## 8
            ['no','yes'], ## 9
        ]

        # # target encode
        # target_encode = ['Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II','Obesity_Type_I','Obesity_Type_II','Obesity_Type_III']


        # Pipeline
        num_pipeline = Pipeline(
            steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ]
        )

        cat_pipeline = Pipeline(
            steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('encoder',OrdinalEncoder(categories=cat_encode)),
            ]
        )


        resample_pipeline = ColumnTransformer([
            ('num_pipeline',num_pipeline,num_cols),
            ('cat_pipeline',cat_pipeline,cat_cols),
        ])

        
        # Save pipeline as pickle file
        save_pickle(Path(self.config.preprocessor_path),resample_pipeline)

        
    def train(self):
        data = pd.read_csv(self.config.clean_data_path)
        # Split the data
        X = data.drop('NObeyesdad',axis=1)
        y = data['NObeyesdad']

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

        # Fit the model
        clf = RandomForestClassifier()
        clf.fit(X_train,y_train)

        # save Pred results
        y_pred = clf.predict(X_test)

        # Save model as pickle file
        save_pickle(Path(self.config.model_path),clf) 

        # Save metrics as json file
        metrics = {
            # 'confusion_matrix':confusion_matrix(y_test,y_pred).tolist(),
            'Accuracy':accuracy_score(y_test,y_pred),
            'Precision':precision_score(y_test,y_pred,average='weighted'),
            'Recall':recall_score(y_test,y_pred,average='weighted'),
            'F1_score':f1_score(y_test,y_pred,average='weighted')
        }

        save_json(Path(self.config.metrics_path),metrics)
    
    def predict(self,data):
        model_path, transform_path = self.config.model_path, self.config.preprocessor_path

        model = load_pickle(model_path)
        transform_obj = load_pickle(transform_path)

        data_transform = transform_obj.transform(data)

        predict = model.predict(data_transform)
        
        # target encode
        target_encode = ['Insufficient_Weight','Normal_Weight','Overweight_Level_I','Overweight_Level_II','Obesity_Type_I','Obesity_Type_II','Obesity_Type_III']

        return target_encode[predict]
        

if __name__ == '__main__':
    # Example usage
    print(os.getcwd())
    os.chdir('../../')
    config_path = 'config/config.yaml'
    training = Training(config_path)
    training.transform()
    training.train()










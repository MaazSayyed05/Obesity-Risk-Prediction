
import mysql.connector
import os, sys
from pathlib import Path
from obesity_risk_pred.utils import load_json

class mysqlconnect:

    def __init__(self):
        host = "localhost"
        user = "root"
        password = "8767M@@z052003"
        os.chdir('../../')

        self.mydb = mysql.connector.connect(
            host = host, 
            user = user, 
            password = password)

        self.db_name = 'projects'
        self.table_name = 'obesity'

    def create_db_table(self):

        # db_name = 'projects'
        # table_name = 'obesity'

        mycursor = self.mydb.cursor()

        mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_name};')
        mycursor.execute(f'USE {self.db_name};')

        
        schema = load_json('schema.json')

        for col in schema.keys():
            if schema[col] == 'int64':
                schema[col] = 'INT'
            
            elif schema[col] == 'float64':
                schema[col] = 'FLOAT'
            
            elif schema[col] == 'object':
                schema[col] = 'VARCHAR(255)'
        
        create_table = f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INT AUTO_INCREMENT PRIMARY KEY,userName VARCHAR(255),userID VARCHAR(255),'
        for col in schema.keys():
            create_table += f'{col} {schema[col]},'

        create_table = create_table[:-1] + ');'

        mycursor.execute(create_table)
        self.mydb.commit()
        mycursor.close()

    # def insert_data(self,data,predicted):

    def insert_data(self,data,predicted):
        # data will be a list of as per seq of schema elements
        mycursor = self.mydb.cursor()
        
        # os.chdir('../../')
        schema = load_json('schema.json')

        # insert_into = f'INSERT INTO {self.db_name}.{self.table_name} VALUES ('
        # for d in data:
        #     insert_into += f'"{d}",'
        # insert_into += f'"{predicted}");'

        insert_into = f'INSERT INTO {self.db_name}.{self.table_name} (userName,userID,'
        for col in schema.keys():
            insert_into += f'{col},'
        insert_into = insert_into[:-1] + ') VALUES ('
        for d in data:
            insert_into += f'"{d}",'
        insert_into += f'"{predicted}");'

        mycursor.execute(insert_into)
        self.mydb.commit()
        mycursor.close()
    
    def show_data(self):
        mycursor = self.mydb.cursor()
        mycursor.execute(f'SELECT * FROM {self.db_name}.{self.table_name};')
        # print the entire table on app.py

    def search_data(self,ptr,val):
        # if ptr  == 0 search by unserID
        mycursor = self.mydb.cursor()
        if ptr == 0:
            mycursor.execute(f'SELECT * FROM {self.db_name}.{self.table_name} WHERE userID = {val};')
        else:
            mycursor.execute(f'SELECT * FROM {self.db_name}.{self.table_name} WHERE userName = "{val}";')
        
        # print the entire table on app.py
    
    def search_by_result(self, result):
        target = 'NObeyesdad'
        mycursor = self.mydb.cursor()
        mycursor.execute(f'SELECT * FROM {self.db_name}.{self.table_name} WHERE {target} = {result};')

        # print the entire table on app.py
    


if __name__ == '__main__':
    mysql = mysqlconnect()
    mysql.create_db_table()
    # mysql.insert_data(['Umar Sayyed','umar@03','Male',24.443011,1.699998,81.66995,'yes','yes',2.0,2.983297,'Sometimes','no',2.763573,'no',0.0,0.976473,'Sometimes','Public_Transportation'],'Overweight_Level_I')





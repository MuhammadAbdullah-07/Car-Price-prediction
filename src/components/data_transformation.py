from dataclasses import dataclass
import os
import sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder
from sklearn.compose import ColumnTransformer
from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj


@dataclass
class DataTransformationConfig:
    preprocessor_file_obj_path=os.path.join('artifacts','preprocessor.pkl')  

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_transform_data(self):
        try:
            num_feature=['Year','Present_Price','Kms_Driven','Owner','Car_Age'] 

            # Remove Car_Name from cat_feature
            binary_cat_feature = ['Seller_Type', 'Transmission']
            multi_cat_feature = ['Fuel_Type']
            # We'll drop Car_Name in initiate_data_transformation method 

            num_pipeline=Pipeline(
                steps=[('Imputer',SimpleImputer(strategy="median")), ## handle missing values with median
                        ('scaler',StandardScaler())])

            binary_pipeline=Pipeline(
                steps=[('Imputer',SimpleImputer(strategy="most_frequent")), ## handle missing values with most frequent
                       ('OrdinalEncoder',OrdinalEncoder())])
            multi_cat_pipeline=Pipeline(
                steps=[('Imputer',SimpleImputer(strategy="most_frequent")), ## handle missing values with most frequent
                       ('OneHotEncoder',OneHotEncoder())])            
            
            logging.info("Num columns encoding completed")
            logging.info("Cat columns encoding completed")
            preprocessor=ColumnTransformer(transformers=[
            ('num_pipeline',num_pipeline,num_feature),
            ('binary_pipeline',binary_pipeline,binary_cat_feature),
            ('multi_cat_pipeline',multi_cat_pipeline,multi_cat_feature)  ])

            logging.info("Pipeline Transforamtion Completed !")
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)     


    def initaiate_data_transformation(self,train_path,test_path):
        try:
            
            train_df= pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Train & test data reading completed")

            logging.info("Now obtaining preprocessor object")
            preprocessor_obj=self.get_transform_data()

            ## Dividing df into X & y
            target_column = 'Selling_Price'

            ## Training data
            X_train = train_df.drop(columns=[target_column, 'Car_Name'])
            y_train=train_df[target_column]

            ## Test data
            X_test=test_df.drop(columns=[target_column, 'Car_Name'])
            y_test=test_df[target_column]

            # Step 4: Apply preprocessor X_train and X_test
            X_train_transformed = preprocessor_obj.fit_transform(X_train)
            X_test_transformed = preprocessor_obj.transform(X_test)

            # Step 5: Combing X and y
            train_arr=np.c_[X_train_transformed,np.array(y_train)]
            test_arr=np.c_[X_test_transformed,np.array(y_test)]

            # Step 6: Save obj
            save_obj(
                file_path=self.data_transformation_config.preprocessor_file_obj_path,
                obj=preprocessor_obj
            )
            logging.info("Preprocessor saved successfully")

            return train_arr, test_arr,self.data_transformation_config.preprocessor_file_obj_path




        except Exception as e:
            raise CustomException(e,sys)       
        
import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_obj

class PredictPipeline:
    def __init__(self):
        pass

    def Predict(self,features):
        try:
            model_path='artifacts/model.pkl'  ## Assigning Variable to model
            preprocessor_path='artifacts/preprocessor.pkl'  ## Assigning Variable to preprocessor
            model=load_obj(model_path) ## Loading the model
            preprocessor=load_obj(preprocessor_path) ## Loading the preprocessor
            scaled_data=preprocessor.transform(features)
            preds=model.predict(scaled_data)

            return preds

        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
                 year: int,
                 present_price: float,
                 kms_driven: int,
                 fuel_type: str,
                 seller_type: str,
                 transmission: str,
                 owner: int,
                 car_age: int):

        self.year = year
        self.present_price = present_price
        self.kms_driven = kms_driven
        self.fuel_type = fuel_type
        self.seller_type = seller_type
        self.transmission = transmission
        self.owner = owner
        self.car_age = car_age

    def get_data_as_dataframe(self):
        try:
            custom_data_dict = {
                "Year": [self.year],
                "Present_Price": [self.present_price],
                "Kms_Driven": [self.kms_driven],
                "Fuel_Type": [self.fuel_type],
                "Seller_Type": [self.seller_type],
                "Transmission": [self.transmission],
                "Owner": [self.owner],
                "Car_Age": [self.car_age]
            }
            return pd.DataFrame(custom_data_dict)

        except Exception as e:
            raise CustomException(e, sys)
        
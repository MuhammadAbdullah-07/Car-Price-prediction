## Takes train_arr and test_arr
## Trains multiple models
## Evaluates each model
## Saves the best model as model.pkl

from dataclasses import dataclass
import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge,Lasso,ElasticNet
from sklearn.ensemble import RandomForestRegressor ,GradientBoostingRegressor
from src.utils import save_obj, evaluate_models
from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig:
    trained_model_path=os.path.join('artifacts','model.pkl') 

class ModelTrainer:
    def __init__(self):
        self.trained_model_config=ModelTrainerConfig()

    def initaite_model_trainer(self,train_arr,test_arr): ## we inherit it here from transformation. while link them in root (data_ingestion)
        try:
            logging.info("split Train and test input data")            
            X_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            X_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            models={
                "LinearRegression": LinearRegression(),
                "RidgeRegression":Ridge() ,
                "LassoRegression": Lasso(),
                "ElasticNet": ElasticNet(),
                "RandomForest":RandomForestRegressor(),
                "GradientBoosting" : GradientBoostingRegressor()  
            }

            params={
                "LinearRegression":{},
                "RidgeRegression":{
                    'alpha': [0.001, 0.01, 0.1, 1, 10, 100, 1000]
                },
                "LassoRegression":{
                    'alpha': [0.001, 0.01, 0.1, 1, 10, 100]
                },
                "ElasticNet":{
                    'alpha': [0.001, 0.01, 0.1, 1, 10],
                    'l1_ratio': [0.1, 0.3, 0.5, 0.7, 0.9],
                    'max_iter': [1000, 5000]                    
                },
                "RandomForest" : {
                    'n_estimators': [50, 100, 200, 300],
                    'max_depth': [3, 5, 10, 15, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]                    
                },
                "GradientBoosting":{
                    'n_estimators': [50, 100, 200, 300],
                    'learning_rate': [0.001, 0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7, 9],
                    'subsample': [0.8, 0.9, 1.0]
                }
            }

            model_report=evaluate_models(X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,models=models,params=params)

            ## Get best model Value
            best_model_score = max(sorted(model_report.values()))

            ## Get best model Name
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            # Save best model
            save_obj(
                file_path=self.trained_model_config.trained_model_path,
                obj=best_model
                )

            return best_model_score,best_model_name

        except Exception as e:         
            raise CustomException(e,sys)
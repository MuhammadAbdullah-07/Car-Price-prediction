## It contains common/helper functions that are used across the whole project like:
##    Saving a model to a file (save_object)
##    Loading a model from a file (load_object)
##    Evaluating multiple models and returning best one (evaluate_models)

import os
import sys
import dill 
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

def save_obj(file_path,obj):
    ##  file_path → where to save the file e.g. artifacts/model.pkl
    ## obj → the object to save e.g. trained model

    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        ## Creates artifacts folder if it doesn't exist

        with open(file_path ,'wb') as file_obj:
            dill.dump(obj,file_obj)  ##  Saves the object (obj) into the opened file    

    except Exception as e:
        raise CustomException(e,sys)   

## evaluate Model
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}

        for model_name,model in models.items():
            param= params[model_name]

            grid = GridSearchCV(model,param, cv= 3)
            grid.fit(X_train,y_train)

            ## Getting Best Params And Setting it on Model
            model.set_params(**grid.best_params_)

            ## Train Model
            model.fit(X_train,y_train)

            ## Prediction
            y_train_pred= model.predict(X_train)
            y_test_pred= model.predict(X_test)

            ## R2 Score
            train_score= r2_score(y_train,y_train_pred)
            test_score = r2_score(y_test,y_test_pred)

            report[model_name] = test_score
            logging.info(f"{model_name} → Training Score: {train_score}, Test Score: {test_score}")

        return report    

    except Exception as e:
        raise CustomException(e,sys)
                



## To Load Obj
def load_obj(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e,sys)    




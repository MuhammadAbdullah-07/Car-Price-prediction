from dataclasses import dataclass
import sys
import os
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from src .components.data_transformation import DataTransformation,DataTransformationConfig
from src.components.model_trainer import ModelTrainer

##  @dataclass decorator is used for config classes
@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initaite_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('src/components/notebooks/data/car_data.csv')
            logging.info("Dataset read as dataframe")

            ## Msking artifacts directory
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            ## Save Raw Data
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("Raw data saved successfully")

            ## Train Test Split
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            logging.info("Train Test Split initaited")

            # Step 4: Save train and test
            train_set.to_csv(self.ingestion_config.train_data_path, index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False,header=True)

            # Step 5: Return paths
            return(
            self.ingestion_config.train_data_path,
            self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_path,test_path=obj.initaite_data_ingestion()
    print(train_path,test_path)

    data_transformation=DataTransformation()
    train_arr,test_arr,preprocessor_path=data_transformation.initaiate_data_transformation(train_path,test_path)

    model_trainer= ModelTrainer()
    r2=model_trainer.initaite_model_trainer(train_arr,test_arr)
    print(f"Best model score is :",r2)

    print(train_arr.shape) ## train data
    print(test_arr.shape)  ## test data
    print(preprocessor_path)  ## preprocessor.pkl
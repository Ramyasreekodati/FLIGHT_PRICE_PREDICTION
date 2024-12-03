import pandas as pd
import os
from Flight_Price.logging import logger
from sklearn.ensemble import RandomForestRegressor
from Flight_Price.entity.config_entity import ModelTrainerConfig
import joblib

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

        ml_model=RandomForestRegressor(max_depth=30, max_features='sqrt', min_samples_split=10,n_estimators=400)
        ml_model.fit(train_x,train_y)

        joblib.dump(ml_model, os.path.join(self.config.root_dir, self.config.model_name))
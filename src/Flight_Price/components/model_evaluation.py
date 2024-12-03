import os
import pandas as pd
from sklearn import metrics
from urllib.parse import urlparse
import numpy as np
import joblib
from pathlib import Path
from Flight_Price.utils.common import save_json
from Flight_Price.entity.config_entity import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def predict(self,actual,predicted):
        MAE = metrics.mean_absolute_error(actual,predicted)
        MSE = metrics.mean_squared_error(actual,predicted)
        RMSE = (np.sqrt(metrics.mean_squared_error(actual,predicted)))
        R2_Score = metrics.r2_score(actual,predicted)
        MAPE =metrics.mean_absolute_percentage_error(actual,predicted)

        return MAE,MSE,RMSE,R2_Score,MAPE
    
    def save_results(self):
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)
        
        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]
        
        predicted_qualities = model.predict(test_x)

        (MAE,MSE, RMSE ,R2_Score,MAPE) = self.predict(test_y, predicted_qualities)
        
        # Saving metrics as local
        scores = {"MAE":MAE,"MSE" : MSE,"RMSE" : RMSE ,"R2_Score" : R2_Score,"MAPE" :MAPE}
        save_json(path=Path(self.config.metric_file_name), data=scores)
        
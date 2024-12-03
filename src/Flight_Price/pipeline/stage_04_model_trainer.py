from Flight_Price.config.configuration import ConfigurationManager
from Flight_Price.components.model_trainer import ModelTrainer
from Flight_Price.logging import logger
from pathlib import Path


STAGE_NAME = "Model Trainer stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass


    def main(self):


        try:
            config = ConfigurationManager()
            model_trainer_config = config.get_model_trainer_config()
            model_trainer_config = ModelTrainer(config=model_trainer_config)
            model_trainer_config.train()
        except Exception as e:
            raise e
        


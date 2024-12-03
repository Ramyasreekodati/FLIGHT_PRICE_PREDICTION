from Flight_Price.config.configuration import ConfigurationManager
from Flight_Price.components.data_transformation import DataTransformation
from Flight_Price.logging import logger
from pathlib import Path


STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass


    def main(self):


        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.train_test_spliting()
        except Exception as e:
            raise e

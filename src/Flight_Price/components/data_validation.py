import os
from Flight_Price.logging import logger
import urllib.request as request
import zipfile
from Flight_Price.utils.common import get_size
from Flight_Price.entity.config_entity import DataValidationConfig
from pathlib import Path

import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            for col in all_cols:
                # Check if column is in the schema
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

                # Layer to validate if the datatype is 'object'
                is_object = data[col].dtype == 'object'
                with open(self.config.STATUS_FILE, 'a') as f:
                    f.write(f"Column: {col} , Is Object: {is_object}\n")

            return validation_status

        except Exception as e:
            raise e
from Flight_Price.entity.config_entity import DataIngestionConfig
from Flight_Price.utils.common import read_yaml,create_directories
from Flight_Price.constants.__int__ import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,  # Path to the main config file
        params_filepath = PARAMS_FILE_PATH,  # Path to the parameters file
        schema_filepath = SCHEMA_FILE_PATH  # Path to the schema file
    ):
        self.config = read_yaml(config_filepath)  # Load configuration settings
        self.params = read_yaml(params_filepath)  # Load parameter settings
        self.schema = read_yaml(schema_filepath)  # Load schema details

        create_directories([self.config.artifacts_root]) 
    def get_data_ingestion_config(self) -> DataIngestionConfig:  # Returns data ingestion configuration
        config = self.config.data_ingestion  # Access data ingestion settings

        create_directories([config.root_dir])  # Ensure the root directory for data ingestion exists

        # Populate and return the DataIngestionConfig object with relevant paths and URLs
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config    
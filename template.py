import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s:')


project_name = "Flight_Price"

list_of_files=[
    f"src/{project_name}/__int__.py",
    f"src/{project_name}/components/__int__.py",
    f"src/{project_name}/utils/__int__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__int__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipline/__init__.py",
    f"src/{project_name}/entity/__int__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__int__.py",
    "Config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "template/index.html"
]


for filepath in list_of_files:
    filepath = Path(filepath)  # Converts the string filepath into a Path object
    filedir, filename = os.path.split(filepath)  # Splits the filepath into directory and filename

    # *******If the directory doesn't exist, create it********
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)  # Creates the directory if it doesn't exist, doesn't raise an error if it already exists
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    # *******If the file doesn't exist or is empty, create it*********
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0): # if the file is not exists or file size is 0 create the file other than don't creat it 
        with open(filepath, "w") as f:
            pass  # Just creates an empty file
        logging.info(f"Creating empty file: {filepath}")

    # If the file already exists and isn't empty
    else:
        logging.info(f"{filename} already exists")

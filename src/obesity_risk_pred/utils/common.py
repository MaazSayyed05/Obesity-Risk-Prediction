

import pandas as pd
import os, sys
from pathlib import Path
# from ensure import ensure_annotations ## /
import yaml # 
import json
import joblib
import pickle

# from box import ConfigBox

from typing import Any

import base64



# @ensure_annotations
def read_yaml(path_to_yaml: Path):
    """Read a yaml file and return a ConfigBox object.

    Parameters:
    path_to_yaml : Path

    Returns:
    ConfigBox

    """

    path_to_yaml = Path(path_to_yaml)
    with open(path_to_yaml, "r") as yaml_file:
        content = yaml.safe_load(yaml_file)
        # logging.info(f"yaml file: {path_to_yaml} loaded successfully.")
        return (content)



# @ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates list of directories

    Arguments: path_to_directories

    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)

        if verbose:
            # logging.info(f"Created Directory at {path}.")
            pass


# @ensure_annotations
def save_csv(path: Path, data: pd.DataFrame):
    """
    save csv data

    Args:
    path(Path): path to save csv
    data(pd.DataFrame): data to be save to csv file

    """
    data.to_csv(path, index=False)
    # logging.info(f"csv file saved at: {path}.")
    # return path


# @ensure_annotations
def save_json(path: Path, data: dict):
    """
    save json data

    Args:
    path(Path): path to save json
    data(dict): data to be save to json file

    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    # logging.info(f"json file saved at: {path}.")


# @ensure_annotations
def load_json(path: Path):
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    # logging.info(f"json file loaded succesfully from: {path}")
    return (content)


# @ensure_annotations
def save_pickle(file_path, obj):

    dir_path = os.path.dirname(file_path)

    os.makedirs(dir_path, exist_ok=True)

    with open(file_path, "wb") as file_obj:
        pickle.dump(obj, file_obj)  # file_obj as file_path


# @ensure_annotations
def load_pickle(file_path):

    with open(file_path, "rb") as file_obj:
        return pickle.load(file_obj)

# @ensure_annotations
def save_joblib(file_path: str, obj):
    """
    Save an object to a file using joblib.
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)

    joblib.dump(obj, file_path)  # Directly save the object to the specified file path

# @ensure_annotations
def load_joblib(file_path: str):
    """
    Load an object from a joblib file.
    """
    return joblib.load(file_path)  # Directly load the object from the specified file path



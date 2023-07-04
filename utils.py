import os
from datetime import datetime, timedelta
from typing import Dict
import shutil
import zipfile
from pandas import DataFrame
import csv
from tqdm.auto import tqdm
from src.settings import REPORTS_FOLDER_PATH


def create_vendor_files(query: str, data: DataFrame, vendors: list, timestamp: str) -> None:
    """Walks through a directory and, for each .txt file encountered, adds it to a .zip archive.

    Args:
        query (str): description of the data.
        data (DataFrame): data to be separated in files.
        vendors (list): list of vendors used to filter the data.
        timestamp (str): string with the date and time of the process.
     """
    for vendor in tqdm(vendors, desc=query):
        filename = query + '_nike_' + vendor + '_' +  timestamp + '.txt'    
        data[data['NUMPROVEEDOR'] == vendor].to_csv(
            REPORTS_FOLDER_PATH + '\\' + filename,
            sep=';',
            index=False,
            quoting=csv.QUOTE_NONNUMERIC
        )

def zip_directory(directory_path: str, output_path: str) -> None:
    """Walks through a directory and, for each file encountered, adds it to a zip archive.

    Args:
        directory_path (str): path to the directory that contains the files to zip.
        output_path (str): ath to the output zip file.
     """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory_path))

def remove_files(directory_path: str) -> None:
    """Removes the .txt files created after being saves in a .zip file

    Args:
        directory_path (str): path to the directory that contains the .txt files to be removed.    
    """
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            os.remove(file_path)


def create_files(queries: Dict) -> None:
    """Creates the .txt files and then adds them to a .zip archive

    Args:
        queries (Dict): dictionary with the names of the queries as keys and the data as values.
    """
    timestamp = (datetime.now() - timedelta(days=1)).strftime("%d_%m_%Y_%H_%M_%S")
    
    for query in tqdm(queries, desc="Zipping files..."):
        df = queries[query]
        vendors = df['NUMPROVEEDOR'].drop_duplicates().to_list()
        create_vendor_files(query, df, vendors, timestamp)

        filename = query + '_nike_' + timestamp + '.zip'
        filepath = REPORTS_FOLDER_PATH
        zip_file = os.path.join(filepath, filename)
        zip_directory(filepath, zip_file)

        remove_files(filepath)

def backup_files(directory_path: str, backup_path: str) -> None:
    """Moves the generated .zip files to a backup folder.

    Args:
        directory_path (str): path to the directory that contains the files to be moved.
        backup_path (str): path to the backup directory
    """
    for filename in tqdm(os.listdir(directory_path), desc="Zip Files Backup"):
        if filename.endswith('.zip'):
            source_path = os.path.join(directory_path, filename)
            destination_path = os.path.join(backup_path, filename)
            shutil.move(source_path, destination_path)

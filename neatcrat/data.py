'''
Data('0.csv') gets the data and label files (with the same name) from DATA_DIRECTORY and LABELS_DIRECTORY
Data.all_file_names gets all available file names that corresponds to both a data and a label
'''

import os
import pandas as pd

class Data:

    # where all data csvs are stored
    DATA_DIRECTORY = 'dataset/data'
    LABELS_DIRECTORY = 'dataset/labels'

    # all files in the data and label directory
    data_file_names = os.listdir(DATA_DIRECTORY)
    label_file_names = os.listdir(LABELS_DIRECTORY)

    # all file names that exist both in the data and label directory
    # if a file name exist in both paths, they contain data and label information for the same video.
    all_file_names = set(data_file_names).intersection(set(label_file_names))

    def __init__(self, file_name, dataset_path='.'):

        # do not allow a non-existent file name
        if file_name not in Data.all_file_names:
            raise Exception(f'Cannot construct Data({file_name}) because the file does not exist')
        
        self.file_name = file_name
        
        # get the full path of the specified data and label file
        data_file_path = os.path.join(dataset_path, Data.DATA_DIRECTORY, file_name)
        label_file_path = os.path.join(dataset_path, Data.LABELS_DIRECTORY, file_name)

        # "dfs" is a list of "df"s ordered by timestamp, each "df" contains agent information (organized in rows)
        self.dfs = [df for _, df in sorted(pd.read_csv(data_file_path).groupby('TIMESTAMP'))]

        # label dataframe contains first_class, second_class, and third_class for each timestamp index
        self.label_df = pd.read_csv(label_file_path)

    
    def __str__(self):
        return f'Data({self.file_name})'
    
    def __repr__(self):
        return self.__str__()

    
            

        
            
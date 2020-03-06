"""
Load the config file and create any custom variables
that are available for ease of use purposes
"""

import yaml
import os

BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

with open(BASE_DIR + "/config/config.yml", "r") as configFile:
    data = configFile.read()

data = yaml.load(data, Loader=yaml.FullLoader)

# ORCS config
if data['orcs']['access_key'] == "":
    ACCESS_KEY = os.environ['BIOGRID_ACCESSKEY']
else:
    ACCESS_KEY = data['orcs']['access_key']
BASE_URL = data['orcs']['base_url']

# Results config
RESULTS_FOLDER = data['results']['folder_path']
DIAGRAM_FILE_NAME = data['results']['diagram_file_name']
INPUT_DATA_CSV_NAME = data['results']['input_data_csv_name']
CLUSTER_DATA_TXT_NAME = data['results']['cluster_data_txt_name']
CLUSTER_DATA_CSV_FOLDER = data['results']['cluster_data_csv_folder']
CLUSTER_DATA_CSV_PREFIX = data['results']['cluster_data_csv_prefix']

# Plot config
PLOT_TITLE = data['results']['plot']['title']
PLOT_X_LABEL = data['results']['plot']['x_label']
PLOT_Y_LABEL = data['results']['plot']['y_label']

# Clustering config
MAX_DISTANCE = data['clustering']['max_distance']
PRUNING = data['clustering']['pruning']

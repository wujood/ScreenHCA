from python.output.output import *
from python.api import screens
from python.clustering import training
from python.core import config as cfg

from pathlib import Path
import sys


def main():
    # Read filename from parameters
    filename = sys.argv[1]
    print(filename)
    try:
        with open(filename, 'r', newline="") as file:
            input_screen = json.load(file)
    except IOError:
        print("file path missing")
        return -1

    # Prepare Results Folder
    Path(cfg.RESULTS_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(cfg.CLUSTER_DATA_CSV_FOLDER).mkdir(parents=True, exist_ok=True)

    # Fetch data
    screen_array = screens.get_screens()

    # Add input screen to data if its not one of BioGRID's screens
    input_screen_in_biogrid_data = False
    for screen in screen_array:
        if screen['SCREEN_ID'] == input_screen['SCREEN_ID']:
            input_screen_in_biogrid_data = True
            break
    if not input_screen_in_biogrid_data:
        screen_array.append(input_screen)

    # Extract features, screen_array now holds only screens with valid features
    features, screen_array = screens.get_features(screen_array)
    columns = screen_array[0].keys()
    # Export raw input data as csv
    csv_path = cfg.RESULTS_FOLDER + "/" + cfg.INPUT_DATA_CSV_NAME
    save_csv(csv_path, columns, screen_array)

    # Train model
    model = training.train(features.data_scaled)

    # Plot Results
    training.plot(model, cfg.MAX_DISTANCE, cfg.PRUNING)
    training.save_fig(model, cfg.MAX_DISTANCE, cfg.PRUNING, cfg.RESULTS_FOLDER + '/' + cfg.DIAGRAM_FILE_NAME)

    # Create cluster matrix
    cluster_matrix = training.create_cluster_matrix(model, screen_array)

    # Write clusters to txt file
    cluster_data_file_path = cfg.RESULTS_FOLDER + "/" + cfg.CLUSTER_DATA_TXT_NAME
    save_cluster_matrix_as_txt(cluster_data_file_path, cluster_matrix)

    # Write clusters to csv file(s)
    cluster_csv_path_with_prefix = cfg.CLUSTER_DATA_CSV_FOLDER + "/" + cfg.CLUSTER_DATA_CSV_PREFIX
    for index, cluster in enumerate(cluster_matrix):
        file_path = cluster_csv_path_with_prefix + str(index + 1) + ".csv"
        save_csv(file_path, columns, cluster)

    # Print file content to console
    print(open(cluster_data_file_path).read())

    # Print the cluster the input is in
    print(
        "The given input screen with ID " + input_screen['SCREEN_ID'] + " is contained in cluster " +
        str(training.find_cluster_index_entry(cluster_matrix, input_screen)) + ".")


if __name__ == "__main__":
    main()

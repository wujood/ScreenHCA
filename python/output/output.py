"""
Save results to output files
"""
import csv
import json


def save_csv(path, columns, dict_data):
    dict_data = sanitize_dict(dict_data)
    try:
        with open(path, 'w', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns, delimiter=';')
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def save_cluster_matrix_as_txt(file_path, cluster_matrix):
    cluster_data_file = open(file_path, "w+")
    for index, cluster in enumerate(cluster_matrix):
        cluster_data_file.write('-------------------------------------\r\n')
        cluster_data_file.write('Cluster ' + str(index + 1) + ': ' + str(len(cluster)) + ' items\r\n')
        cluster_data_file.write('-------------------------------------\r\n')
        for entry in cluster:
            cluster_data_file.write(str(entry) + "\r\n")
        cluster_data_file.write("\r\n\r\n")
    cluster_data_file.close()


def sanitize_dict(dict_data):
    json_data = json.dumps(dict_data)
    json_data = json_data.replace("\\n", "")
    json_data = json_data.replace("\\r", "")
    return json.loads(json_data)

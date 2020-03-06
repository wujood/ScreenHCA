# ScreenHCA (SHCA)
![Python package](https://github.com/wujood/ScreenHCA/workflows/Python%20package/badge.svg?branch=master)

# Prerequisites

- Python 3.5+
- Accesskey from BioGRID (https://wiki.thebiogrid.org/doku.php/orcs:webservice)

# Getting Started

Install modules for python with pip:
```shell
cd python
pip install -r requirements.txt
```

Run the following command to test your installation:
```shell
cd python
python ./main.py ./test_input.json
```

# Usage
To find similar screens to a new screen, you can create a new JSON file that contains basic informations about the screening. Below is an example that lists the informations needed (if you see strings that are devided by a `|` it means that you have to choose one of the supported strings, feel free to open an issue if there is a missing choice):
```json
{
  "SCREEN_ID": "<integer (if it is a new screen you can type '-1' here)>",
  "SCORES_SIZE": "<integer>",
  "FULL_SIZE": "<integer>",
  "NUMBER_OF_HITS": "<integer>",
  "SCREEN_TYPE": "Negative Selection | Positive Selection | Phenotype Screen",
  "DURATION": "<integer> Days",
  "METHODOLOGY": "Knockout | Inhibition | Activation",
  "ENZYME": "CAS9 | d-Cas9-KRAB | SAM (NLS-dCas9-VP64/MS2-p65-HSF1) | sunCas9"
}
```
Once you created the JSON file you can run the script with the path to the file as a parameter:
```shell
# From the root folder of this repo
cd python
python ./main.py ./your-file.json
```
From there you can see the clustering visualized and you can find CSV files in the results folder that show the separate clusters as well as a PNG file of the diagram for later use.

# Configuration
The file `./python/config/config.yaml` can be edited to change behaviours and wordings. **The `access_key` field must be set to a valid key in order for this script to work!** You can generate a new access key here: https://orcsws.thebiogrid.org
```yaml
orcs:
  access_key: "<enter secret here or set BIOGRID_ACCESSKEY as environment variable>"
  base_url: "https://orcsws.thebiogrid.org"

clustering:
  pruning: 4
  max_distance: 11

results:
  folder_path: "./results"
  diagram_file_name: "diagram.png"
  plot:
    title: "Agglomerative Clustering with pruning = 4 and max. distance threshold = 11"
    x_label: "Number of points in node (or index of point if no parenthesis)"
    y_label: "Distance"
  input_data_csv_name: "input_data.csv"
  cluster_data_txt_name: "cluster_data.txt"
  cluster_data_csv_folder: "./results/clusters"
  cluster_data_csv_prefix: "cluster-"
```

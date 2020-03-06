from python.core import config as cfg

import numpy as np
import time
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt
from sklearn.neighbors import kneighbors_graph
from scipy.cluster.hierarchy import fcluster


def create_linkage_matrix(model):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    return np.column_stack([model.children_, model.distances_, counts]).astype(float)


def train(dataset):
    # setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

    return model.fit(dataset)


def create_plot(model, max_distance, pruning):
    linkage_matrix = create_linkage_matrix(model)
    plt.figure(figsize=(20, 10))
    if max_distance:
        plt.axhline(y=max_distance, color='black', linestyle='--')
    plt.title(cfg.PLOT_TITLE)
    dendrogram(linkage_matrix, truncate_mode='level', p=pruning)
    plt.xlabel(cfg.PLOT_X_LABEL)
    plt.ylabel(cfg.PLOT_Y_LABEL)


def plot(model, max_distance, pruning):
    # Create linkage matrix and then plot the dendrogram
    create_plot(model, max_distance, pruning)
    plt.show()


def save_fig(model, max_distance, pruning, path):
    # Create linkage matrix and then save the dendrogram to png file
    create_plot(model, max_distance, pruning)
    plt.savefig(path)


def graph(x, n_clusters):
    # Create a graph capturing local connectivity. Larger number of neighbors
    # will give more homogeneous clusters to the cost of computation
    # time. A very large number of neighbors gives more evenly distributed
    # cluster sizes, but may not impose the local manifold structure of
    # the data
    knn_graph = kneighbors_graph(x, 1, include_self=False)

    for connectivity in (None, knn_graph):
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 4, 0 + 1)
        model = AgglomerativeClustering(connectivity=connectivity,
                                        n_clusters=n_clusters)
        model.fit(x)
        plt.scatter(x[:, 0], x[:, 1], c=model.labels_,
                    cmap=plt.cm.get_cmap("Spectral"))
        plt.axis('equal')
        plt.axis('off')

        plt.subplots_adjust(bottom=0, top=.89, wspace=0,
                            left=0, right=1)
        plt.suptitle('n_cluster=%i, connectivity=%r' %
                     (n_clusters, connectivity is not None), size=17)
    plt.show()


def get_cluster_labels(linkage_matrix, max_distance, criterion):
    cluster_labels = fcluster(linkage_matrix, max_distance, criterion=criterion)
    return cluster_labels


def find_cluster_index_entry(cluster_matrix, searched_entry):
    searched_entry_id = searched_entry['SCREEN_ID']
    for cluster_index, cluster in enumerate(cluster_matrix):
        for entry in cluster:
            if entry['SCREEN_ID'] == searched_entry_id:
                # First cluster is 1, not 0
                return cluster_index + 1
    return -1


def create_cluster_matrix(model, data):

    # Create linkage matrix & extract cluster groups
    matrix = create_linkage_matrix(model)
    cluster_labels = get_cluster_labels(matrix, cfg.MAX_DISTANCE, 'distance')
    cluster_count = max(cluster_labels)

    # Create cluster matrix
    cluster_matrix = []
    for cluster_label in range(1, cluster_count + 1):
        cluster = []
        cluster_indices = [i for i, e in enumerate(cluster_labels) if e == cluster_label]
        for i in cluster_indices:
            cluster.append(data[i])
        cluster_matrix.append(cluster)
    return cluster_matrix

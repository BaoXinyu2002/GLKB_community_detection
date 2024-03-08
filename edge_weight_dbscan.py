import pandas as pd
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import laplacian
# from scipy.linalg import eigh
from sklearn.cluster import DBSCAN
from scipy.sparse.linalg import eigs
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.neighbors import sort_graph_by_row_values
import csv
import os
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import argparse
from pathlib import Path

# Initialize the argument parser
parser = argparse.ArgumentParser(description="DBSCAN with Openai embedding.")
# Add an argument for the input file path
parser.add_argument("input_edge_file", type=str, help="Path to the input edge file")
parser.add_argument("output_stats", type=str, help="Path to the output statistic file")
parser.add_argument("eps", type=float, default=0.5, help="Maximum distance between two nodes in a cluster")
parser.add_argument("min_samples", type=int, default=5, help="Minimum number of nodes in a cluster")

def weight_to_distance(matrix):
    distance_matrix = matrix.copy()
    with np.errstate(divide='ignore', invalid='ignore'):
        distance_matrix.data = 1.0 / distance_matrix.data
        distance_matrix.data[np.isinf(distance_matrix.data)] = 6
    return distance_matrix


edges = pd.read_csv(input_edge_file, sep=',' )
edges_logmap=edges[edges['Source']=='logmapml']
edges_logmap=edges_logmap[edges_logmap['Score']>=0.4]

G_logmap = nx.Graph()
for idx, row in edges_logmap.iterrows():
    G_logmap.add_edge(row['Head Curie'], row['Tail Curie'], weight=row['Score'])

edges_in_graphs = set()
for edge in G_logmap.edges():
    sorted_edge = tuple(sorted(edge))
    edges_in_graphs.add(sorted_edge)
total_edges_in_original_graph = len(edges_in_graphs)

adjacency_matrix = nx.to_scipy_sparse_array(G_logmap, weight='weight',format='csr')
distance_matrix = weight_to_distance(adjacency_matrix)
sorted_distance_matrix = sort_graph_by_row_values(distance_matrix)


# adjacency_matrix = StandardScaler(with_mean=False).fit_transform(adjacency_matrix)
dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
clusters = dbscan.fit_predict(sorted_distance_matrix)

silhouette_avg = silhouette_score(sorted_distance_matrix, clusters)
# calinski_harabasz = calinski_harabasz_score(sorted_distance_matrix, clusters)
# davies_bouldin = davies_bouldin_score(sorted_distance_matrix, clusters)
if not os.path.exists(f"DBSCAN_{eps}_{min_samples}"):
    os.mkdir(f"DBSCAN_{eps}_{min_samples}")
subgraphs = []
for cluster_id in set(clusters):
    if cluster_id != -1:
        nodes_in_cluster = [node for node, cluster in zip(G_logmap.nodes, clusters) if cluster == cluster_id]
        subgraph = G_logmap.subgraph(nodes_in_cluster)
        subgraphs.append(subgraph)

for i, sg in enumerate(subgraphs):
    nx.write_graphml(sg, f"DBSCAN_{eps}_{min_samples}/subgraph_{i}.graphml")
unique_edges_in_subgraphs = set()

for sg in subgraphs:
    for edge in sg.edges():
        sorted_edge = tuple(sorted(edge))
        unique_edges_in_subgraphs.add(sorted_edge)

total_unique_edges_in_subgraphs = len(unique_edges_in_subgraphs)

coverage_ratio = total_unique_edges_in_subgraphs / total_edges_in_original_graph

with open(output_stats,"a") as file:
    writer = csv.writer(file)
    writer.writerow([f"{eps},{min_samples}",total_unique_edges_in_subgraphs,total_edges_in_original_graph,coverage_ratio,silhouette_avg])
print(total_edges_in_original_graph)
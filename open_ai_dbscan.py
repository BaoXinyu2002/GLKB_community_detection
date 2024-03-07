import networkx as nx
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import json
import csv
import os
from sklearn.metrics import silhouette_score
from node2vec import Node2Vec
from pathlib import Path

# Initialize the argument parser
parser = argparse.ArgumentParser(description="DBSCAN with Openai embedding.")
# Add an argument for the input file path
parser.add_argument("input_edge_file", type=str, help="Path to the input edge file")
parser.add_argument("input_embeddings", type=str, help="Path to the input embedding file")
parser.add_argument("output_stats", type=str, help="Path to the output statistic file")
parser.add_argument("eps", type=float, default=0.5, help="Maximum distance between two nodes in a cluster")
parser.add_argument("min_samples", type=int, default=5, help="Minimum number of nodes in a cluster")

# Parse the command line arguments
args = parser.parse_args()

edges = pd.read_csv(input_edge_file, sep=',' )
# edges = edges[edges['Score']>=0.6]

G = nx.Graph()
for idx, row in edges.iterrows():
    G.add_edge(row['Head Curie'], row['Tail Curie'], weight=row['Score'],label=row['Source']) 

total_nodes = G.number_of_nodes()
embeddings_df = pd.read_csv(input_embeddings)
X = embeddings_df.iloc[:, :-1].values
# epss = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
# min_sampless=[5]
# for eps in epss:
#     for min_samples in min_sampless:
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
clusters = dbscan.fit_predict(X)
embeddings_df['cluster'] = clusters
subgraphs = []
for cluster_id in embeddings_df['cluster'].unique():
    if cluster_id != -1:
        cluster_node_ids = embeddings_df[embeddings_df['cluster'] == cluster_id]['id'].astype(str).tolist()
        subgraph = G.subgraph(cluster_node_ids)
        subgraphs.append(subgraph)
if not os.path.exists(f"Openai_DBSCAN_{eps}_{min_samples}"):
    os.mkdir(f"Openai_DBSCAN_{eps}_{min_samples}")
not_covered_nodes=np.count_nonzero(clusters == -1)
for i, sg in enumerate(subgraphs):
    nx.write_graphml(sg, f"Openai_DBSCAN_{eps}_{min_samples}/subgraph_{i}.graphml")
with open(output_stats,"a") as file:
    writer = csv.writer(file)
    writer.writerow([f"{eps},{min_samples}",not_covered_nodes,total_nodes])



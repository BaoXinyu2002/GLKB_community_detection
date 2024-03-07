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


edges = pd.read_csv('/nfs/turbo/umms-drjieliu/usr/xinyubao/umls_matching/database/mappings_without_dup.csv', sep=',' )
# edges = edges[edges['Score']>=0.6]

G = nx.Graph()
for idx, row in edges.iterrows():
    G.add_edge(row['Head Curie'], row['Tail Curie'], weight=row['Score'],label=row['Source']) 


embeddings_df = pd.read_csv("embeddings_with_ids2.csv")
X = embeddings_df.iloc[:, :-1].values
epss = [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
min_sampless=[5]
for eps in epss:
    for min_samples in min_sampless:
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
        try:
            silhouette_avg = silhouette_score(embeddings, clusters)
        except:
            silhouette_avg = 0
        with open("stat_4.csv","a") as file:
            writer = csv.writer(file)
            writer.writerow([f"{eps},{min_samples}",silhouette_avg,not_covered_nodes])



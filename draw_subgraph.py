import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

id_label_df = pd.read_csv('id_label_2.csv')

id_to_label = pd.Series(id_label_df.Label.values, index=id_label_df.ID).to_dict()

for i in range(3292):

    G = nx.read_graphml(f'/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.5_5/subgraph_{i}.graphml')
    combined_labels = {}
    for node in G.nodes():
        node_id = str(node)
        label = id_to_label.get(node_id, '')  
        combined_labels[node] = f"{node_id}\n{label}"

    plt.figure(figsize=(12, 10))
    nx.draw(G, labels=combined_labels, with_labels=True, node_size=700, node_color='lightblue', font_size=8, font_weight='bold')
    plt.title('Graph Visualization with IDs and Labels')
    # plt.show()
    plt.savefig(f'/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.5_5/subgraph_{i}.png', dpi=300, bbox_inches='tight')
    plt.close()
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Visualize subgraph.")
# Add an argument for the input file path
parser.add_argument("input_file", type=str, help="Path to the input id_label file")
parser.add_argument("input_subgraph", type=str, help="Path to the input subgraph directory file")
# Parse the command line arguments
args = parser.parse_args()

id_label_df = pd.read_csv(input_file)

id_to_label = pd.Series(id_label_df.Label.values, index=id_label_df.ID).to_dict()

pathlist = Path(input_subgraph).rglob('*.graphml')
for path in pathlist:
    path_str = str(path)
    G = nx.read_graphml(path_str)
    combined_labels = {}
    for node in G.nodes():
        node_id = str(node)
        label = id_to_label.get(node_id, '')  
        combined_labels[node] = f"{node_id}\n{label}"

    plt.figure(figsize=(12, 10))
    nx.draw(G, labels=combined_labels, with_labels=True, node_size=700, node_color='lightblue', font_size=8, font_weight='bold')
    plt.title('Graph Visualization with IDs and Labels')
    # plt.show()
    fig_path=path_str.replace('.graphml','.png')
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
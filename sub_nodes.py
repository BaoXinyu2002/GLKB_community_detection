import xml.etree.ElementTree as ET
import csv
import os
import glob
from pathlib import Path

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Visualize subgraph.")
# Add an argument for the input file path
parser.add_argument("input_file", type=str, help="Path to the input id_label file")
parser.add_argument("input_subgraph", type=str, help="Path to the input subgraph directory file")
# Parse the command line arguments
args = parser.parse_args()

all_subgraphs_data = []
rep_nodes=[]

pathlist = Path(input_subgraph).rglob('*.graphml')
for path in pathlist:
    path_str = str(path)
    tree = ET.parse(path_str)
    root = tree.getroot()

    namespaces = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}
    representative_node_id = ''

    nodes = []
    edges = []
    representative_node_id = graphml_file.split('/')[-1].split('.')[0]

    rep_nodes.append(representative_node_id)

    for edge in root.findall('.//graphml:edge', namespaces):
        source = edge.get('source')
        target = edge.get('target')
        edges.append((source, target))
        edges.append((representative_node_id, source))
        edges.append((representative_node_id, target))

    for node_id in nodes[:-1]:
        edges.append((node_id, representative_node_id))

    all_subgraphs_data.append((nodes, edges))

edges_path=input_subgraph+'subgraphs_edges.csv'
with open(edges_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Node', 'Connected_Node'])

    for nodes, edges in all_subgraphs_data:
        for edge in edges:
            csvwriter.writerow([edge[0], edge[1]])

nodes_path=input_subgraph+'subgraphs_rep_nodes.csv'
with open(nodes_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Representative_Node_ID'])
    for rep_node_id in rep_nodes:
        csvwriter.writerow([rep_node_id])

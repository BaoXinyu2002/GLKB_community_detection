import xml.etree.ElementTree as ET
import csv
import glob
import os
import argparse

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Get embeddings for texts.")
# Add an argument for the input file path
parser.add_argument("small_subgraph", type=str, help="Path to the directory of small subgraph")
parser.add_argument("large_subgraph", type=str, help="Path to the directory of large subgraph")
parser.add_argument("output_file", type=str, help="Path to the output embedding file")
# Parse the command line arguments
args = parser.parse_args()

def get_representative_node_id(node_ids):
    return '-'.join(sorted(node_ids))

def read_subgraph_nodes(graphml_file, namespaces):
    tree = ET.parse(graphml_file)
    root = tree.getroot()
    node_ids = {node.get('id') for node in root.findall('.//graphml:node', namespaces)}
    return get_representative_node_id(node_ids),node_ids

namespaces = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

small_subgraphs = {}
for graphml_file in glob.glob('/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.2_5/subgraph_*.graphml'):
    subgraph_name = '0.2_'+os.path.basename(graphml_file).split('.')[0]
    sub_rep,node_ids=read_subgraph_nodes(graphml_file, namespaces)
    small_subgraphs[subgraph_name] = node_ids

large_subgraphs = {}
for graphml_file in glob.glob('/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.4_5/subgraph_*.graphml'):
    subgraph_name = '0.5_'+os.path.basename(graphml_file).split('.')[0]
    sub_rep,node_ids=read_subgraph_nodes(graphml_file, namespaces)
    large_subgraphs[subgraph_name] = node_ids

contained_relations = []
for large_sg, large_nodes in large_subgraphs.items():
    for small_sg, small_nodes in small_subgraphs.items():
        # print(large_nodes)
        # print(small_nodes)
        intersection = large_nodes.intersection(small_nodes)
        if len(intersection) / len(small_nodes) >= 0.75:
            contained_relations.append((large_sg, small_sg))

with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Large_Subgraph', 'Contained_Small_Subgraph'])
    for relation in contained_relations:
        csvwriter.writerow(relation)

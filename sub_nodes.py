import xml.etree.ElementTree as ET
import csv
import os
import glob

all_subgraphs_data = []
rep_nodes=[]

for graphml_file in glob.glob('/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.9_5/subgraph_*.graphml'):
    tree = ET.parse(graphml_file)
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

with open('/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.9_5/subgraphs_edges.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Node', 'Connected_Node'])

    for nodes, edges in all_subgraphs_data:
        for edge in edges:
            csvwriter.writerow([edge[0], edge[1]])

with open('/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/Openai_DBSCAN_0.9_5/subgraphs_rep_nodes.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Representative_Node_ID'])
    for rep_node_id in rep_nodes:
        csvwriter.writerow([rep_node_id])

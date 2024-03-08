# GLKB community detection Pipline
## Introduction
This pipline aims to find subgraphs that gather closely in a graph. These subgraphs (i.e. communities) have a closer relationship than other part of the graph. Finding these subgraphs are not only usful for recommanding related items but also important for graph learning models to learn the semantic connections and discover hidden patterns.
## Usage
### Startup
### Preprocess
Suppose we have the node and edge information. We need a curie-label table for nodes, and a head_curie-tail_curie table for edges.

### Step 1: Get Openai Embedding
This is to get the openai embedding for the clustering.

```python3 api_embed.py --input_file your_curie-label_csv_file --api_key your_openai_api_key --output_file your_embedding_file_name```

### Step 2: Generate Subgraphs
This is to get the subgraphs by using DBSCAN algorithm and Openai embeddings.

```python3 open_ai_dbscan.py --input_edge_file your_edge_information --input_embeddings openai_embeddings --output_stats your_file_path_to_store_subgraph_information --eps eps_num --min_samples min_sample_num```

Alternatively, we can get the subgraphs by using DBSCAN algorithm and edge weights.
```python3 edge_weight_dbscan.py --input_edge_file your_edge_information --output_stats your_file_path_to_store_subgraph_information --eps eps_num --min_samples min_sample_num```

### Step 3: Convert Subgraph Information into CSV File
This is to convert the subgraph information into a csv file for further analysis.

```python3 sub_nodes.py --input_subgraph your_subgraph_directory```

### Step 4: Visualization (Optional)
This is to visualize the generated subgraphs to evaluate its accuracy. This will generate a plot for each graph.

```python3 draw_subgraph.py --input_subgraph your_subgraph_directory --input_file your_curie-label_csv_file```

### Step 5: Get the Hierarchical Information
If we generate multiple sets of subgraphs with different parameters(i.e. different eps and min_samples), some smaller subgraphs are likely contained in one large subgraph. This is to find such hierarchical information.

```python3 hierarchy.py --small_subgraph path_to_smaller_subgraph_directory --large_subgraph path_to_larger_subgraph_directory --output_file output_file_path```
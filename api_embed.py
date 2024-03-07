import openai
import pandas as pd
import argparse

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Get embeddings for texts.")
# Add an argument for the input file path
parser.add_argument("input_file", type=str, help="Path to the input id_label file")
parser.add_argument("api_key", type=str, help="API key for embedding")
parser.add_argument("output_file", type=str, help="Path to the output embedding file")
# Parse the command line arguments
args = parser.parse_args()

openai.api_key = api_key

def get_embedding(texts, model="text-embedding-3-small"):
    texts = [str(text).replace("\n", " ") for text in texts]
    response = openai.Embedding.create(input=texts, model=model)
    embeddings = [embedding['embedding'] for embedding in response['data']]
    return embeddings

df = pd.read_csv(input_file)

batch_size = 1000

all_embeddings = []
all_ids = []

for i in range(0, len(df), batch_size):
    batch_df = df[i:i+batch_size]
    batch_labels = batch_df['Label'].tolist()
    # print(batch_labels)
    # break
    batch_ids = batch_df['ID'].tolist()
    batch_embeddings = get_embedding(batch_labels)
    
    all_embeddings.extend(batch_embeddings)
    all_ids.extend(batch_ids)
    
    print(f"Processed batch {i // batch_size + 1}/{(len(df) + batch_size - 1) // batch_size}")

embeddings_df = pd.DataFrame(all_embeddings)
embeddings_df['id'] = all_ids

embeddings_df.to_csv(output_file, index=False)
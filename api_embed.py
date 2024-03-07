import openai
import pandas as pd

openai.api_key = "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"

def get_embedding(texts, model="text-embedding-3-small"):
    texts = [str(text).replace("\n", " ") for text in texts]
    response = openai.Embedding.create(input=texts, model=model)
    embeddings = [embedding['embedding'] for embedding in response['data']]
    return embeddings

df = pd.read_csv("/nfs/turbo/umms-drjieliu/usr/xinyubao/subgraph/id_label_2.csv")

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

embeddings_df.to_csv("embeddings_with_ids2.csv", index=False)
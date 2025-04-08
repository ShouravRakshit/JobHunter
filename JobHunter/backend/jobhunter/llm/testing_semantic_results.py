import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def test_faiss_query(query, index_path, mapping_path, model_name="all-MiniLM-L6-v2", top_k=5):
    """
    Loads the FAISS index and the mapping of job postings, then performs a semantic
    search for the given query, returning the top_k results along with their row index.
    
    Parameters:
      - query (str): The user's search query or short description.
      - index_path (str): Path to the FAISS index file (e.g. 'bert_faiss_index.idx').
      - mapping_path (str): Path to the pickle file with job metadata.
      - model_name (str): SentenceTransformer model to embed the query.
      - top_k (int): Number of nearest neighbors to retrieve.
      
    Returns:
      A list of tuples (row_index, metadata record) for the top_k closest job postings.
    """
    # 1. Load FAISS index
    index = faiss.read_index(index_path)
    
    # 2. Load the metadata mapping
    with open(mapping_path, "rb") as f:
        mapping = pickle.load(f)  # mapping is a list of dicts
    
    # 3. Embed the query with SentenceTransformers
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")
    
    # 4. Search the FAISS index for the top_k nearest neighbors
    distances, indices = index.search(query_embedding, top_k)
    
    # 5. Retrieve the metadata for each index along with its row number.
    results = []
    for idx in indices[0]:
        record = mapping[idx]
        results.append((idx, record))
    
    return results

if __name__ == "__main__":
    query_str = "looking for a data analytics job with over 2 years of experience"
    index_file = "JobHunter/data/bert_faiss_index.idx"
    mapping_file = "JobHunter/data/bert_faiss_mapping.pkl"
    
    top_results = test_faiss_query(query_str, index_file, mapping_file, top_k=5)
    
    print(f"Top results for query: '{query_str}'\n")
    for rank, (row_index, res) in enumerate(top_results, start=1):
        print(f"Rank {rank} (Row {row_index}): {res['title']}")
        # Print a snippet of the cleaned description
        snippet = res.get('cleaned_description', "")[:150] + "..."
        print(f"   {snippet}\n")

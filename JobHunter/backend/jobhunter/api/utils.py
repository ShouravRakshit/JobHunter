# api/utils.py
import pandas as pd
import faiss
import pickle
import numpy as np

# Global variables for ephemeral data storage
JOB_POSTINGS = []
FAISS_INDEX = None
MAPPING = []

def load_job_postings(csv_path="JobHunter/data/jobs_with_experience_normalized_updated.csv"):
    global JOB_POSTINGS
    df = pd.read_csv(csv_path)
    # Convert DataFrame rows to dict
    JOB_POSTINGS = df.to_dict('records')

def load_faiss_index(index_path="JobHunter/data/bert_faiss_index.idx",
                     mapping_path="JobHunter/data/bert_faiss_mapping.pkl"):
    global FAISS_INDEX, MAPPING
    FAISS_INDEX = faiss.read_index(index_path)
    with open(mapping_path, "rb") as f:
        MAPPING = pickle.load(f)

def embed_query(query, model_name="all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    query_vec = model.encode([query]).astype("float32")
    return query_vec

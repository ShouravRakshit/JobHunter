import os
import pandas as pd
import faiss
import pickle
import numpy as np
from django.conf import settings

# Global variables for in-memory storage
JOB_POSTINGS = []
FAISS_INDEX = None
MAPPING = []

def load_job_postings():
    global JOB_POSTINGS
    
    # Path to your CSV
    csv_path = os.path.join(settings.DATA_DIR, "jobs_with_experience_normalized_updated.csv")
    csv_path = os.path.abspath(csv_path)
    print("Loading CSV from:", csv_path)
    
    df = pd.read_csv(csv_path)
    
    # Replace NaN, +∞, -∞ with None so JSON serializer won't crash
    df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
    
    JOB_POSTINGS = df.to_dict('records')
    print(f"Loaded {len(JOB_POSTINGS)} job postings.")

def load_faiss_index():
    """
    Loads the FAISS index and mapping from the data folder.
    The index is expected at:
        C:\Work\JobHunter\JobHunter\data\bert_faiss_index.idx
    The mapping is expected at:
        C:\Work\JobHunter\JobHunter\data\bert_faiss_mapping.pkl
    """
    global FAISS_INDEX, MAPPING
    index_path = os.path.join(settings.DATA_DIR, "bert_faiss_index.idx")
    mapping_path = os.path.join(settings.DATA_DIR, "bert_faiss_mapping.pkl")
    index_path = os.path.abspath(index_path)
    mapping_path = os.path.abspath(mapping_path)
    
    # Debug: print the paths for verification
    print("Loading FAISS index from:", index_path)
    print("Loading FAISS mapping from:", mapping_path)
    
    # Load the FAISS index
    FAISS_INDEX = faiss.read_index(index_path)
    
    # Load the mapping (e.g., a list of job metadata dictionaries)
    with open(mapping_path, "rb") as f:
        MAPPING = pickle.load(f)
        
    print(f"FAISS index loaded with {FAISS_INDEX.ntotal} vectors.")
    print(f"Mapping loaded with {len(MAPPING)} entries.")

def embed_query(query, model_name="all-MiniLM-L6-v2"):
    """
    Embeds the query string using SentenceTransformer and returns a float32 numpy array,
    suitable for FAISS.
    """
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    query_vec = model.encode([query]).astype("float32")
    return query_vec

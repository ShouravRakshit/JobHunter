import os
import pandas as pd
from django.conf import settings

import numpy as np
from django.conf import settings
from sentence_transformers import SentenceTransformer

# Global variables for in-memory storage
JOB_POSTINGS = []
_embedder    = None

def load_job_postings():
    """
    Load the CSV once into memory so /api/jobs is fast.
    """
    global JOB_POSTINGS
    csv_path = os.path.join(settings.DATA_DIR,
                            "jobs_with_experience_normalized_updated.csv")
    df = pd.read_csv(csv_path).replace({np.nan: None,
                                        np.inf: None, -np.inf: None})
    JOB_POSTINGS = df.to_dict('records')
    print(f"[Init] Loaded {len(JOB_POSTINGS)} job postings.")

def embed_query(query, model_name="all-MiniLM-L6-v2"):
    """
    Embed the query once per request.  Model is cached across calls.
    """
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(model_name)
    return _embedder.encode([query]).astype("float32")
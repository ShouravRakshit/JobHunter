import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

def build_faiss_index(input_csv, index_output_path, mapping_output_path,
                      model_name="all-MiniLM-L6-v2"):
    """
    Reads job postings from a CSV file, combines multiple columns (cleaned_description,
    extracted_skills, experience_normalized) into a single text field, generates
    BERT-based embeddings using SentenceTransformers, builds a FAISS index,
    and saves both the index and a mapping of metadata to disk.
    
    Parameters:
      - input_csv (str): Path to the CSV file containing job postings.
      - index_output_path (str): File path where the FAISS index will be saved.
      - mapping_output_path (str): File path where the metadata mapping (pickle) will be saved.
      - model_name (str): The SentenceTransformer model to use (default: "all-MiniLM-L6-v2").
    
    Returns:
      None (the FAISS index and mapping are saved to disk).
    """
    # 1. Load the job postings data
    df = pd.read_csv(input_csv)
    
    #  merges important columns.
    #  "cleaned_description", "extracted_skills", "experience_normalized"
    df["combined_text"] = (
        df["cleaned_description"].fillna("") + " " +
        df["extracted_skills"].fillna("") + " " +
        df["experience_normalized"].fillna("")
    )
    
    texts = df["combined_text"].tolist()
    
    # Initialize the SentenceTransformer model (a BERT-based model)
    model = SentenceTransformer(model_name)
    print(f"Generating embeddings using model '{model_name}' ...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Convert embeddings to float32 for FAISS
    embeddings = np.array(embeddings).astype("float32")
    num_docs, d = embeddings.shape
    print(f"Generated embeddings for {num_docs} documents with dimension {d}.")
    
    # Build a FAISS index (using a simple L2 distance index)
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    print(f"FAISS index built with {index.ntotal} vectors.")
    
    # Save the FAISS index to disk
    faiss.write_index(index, index_output_path)
    print(f"FAISS index saved to {index_output_path}.")
    
    #  Save a mapping of each row to job metadata (e.g., title and combined_text)
    #    so you can retrieve the full posting from a FAISS search result
    mapping = df[['title', "combined_text"]].to_dict('records')
    with open(mapping_output_path, "wb") as f:
        pickle.dump(mapping, f)
    print(f"Mapping saved to {mapping_output_path}.")

def main():
    input_csv = "JobHunter/data/jobs_with_experience_normalized_updated.csv"
    index_output_path = "JobHunter/data/bert_faiss_index.idx"
    mapping_output_path = "JobHunter/data/bert_faiss_mapping.pkl"
    
    build_faiss_index(input_csv, index_output_path, mapping_output_path)

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

def build_faiss_index(input_csv, index_output_path, mapping_output_path,
                      text_column="cleaned_description", model_name="all-MiniLM-L6-v2"):
    """
    Reads job postings from a CSV file, combines important fields (cleaned description,
    and if available, experience_required and technical_skills) into a single text field,
    generates BERT-based embeddings using SentenceTransformers, builds a FAISS index,
    and saves both the index and a mapping of metadata.
    
    This update ensures that technical skill and experience requirements are captured
    in the embeddings for improved semantic search.
    
    Parameters:
      - input_csv (str): Path to the CSV file containing job postings.
      - index_output_path (str): Path where the FAISS index will be saved.
      - mapping_output_path (str): Path where the metadata mapping (pickle) will be saved.
      - text_column (str): Column name containing the base text to embed.
      - model_name (str): Name of the SentenceTransformer model to use.
    
    Returns:
      None (the FAISS index and mapping are saved to disk).
    """
    # Load the data
    df = pd.read_csv(input_csv)
    
    # Create a combined text field that includes the cleaned description and, if available,
    # other important fields such as technical skills and experience requirements.
    # Adjust the field names as per your CSV structure.
    df["combined_text"] = df[text_column].fillna("")
    if "experience_required" in df.columns:
        df["combined_text"] += " " + df["experience_required"].fillna("")
    if "technical_skills" in df.columns:
        df["combined_text"] += " " + df["technical_skills"].fillna("")
    
    texts = df["combined_text"].tolist()
    
    # Initialize the SentenceTransformer model
    model = SentenceTransformer(model_name)
    print(f"Generating embeddings using model '{model_name}' ...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Convert embeddings to a numpy array with type float32 for FAISS.
    embeddings = np.array(embeddings).astype("float32")
    num_docs, d = embeddings.shape
    print(f"Generated embeddings for {num_docs} documents with dimension {d}.")
    
    # Build a FAISS index using a flat L2 distance index.
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    print(f"FAISS index built with {index.ntotal} vectors.")
    
    # Save the FAISS index to disk (this will overwrite previous index file if it exists).
    faiss.write_index(index, index_output_path)
    print(f"FAISS index saved to {index_output_path}.")
    
    # Save a mapping from index (row number) to job metadata (e.g., title, combined_text).
    # This mapping will allow you to retrieve the full job details given a FAISS index result.
    mapping = df[['title', "combined_text"]].to_dict('records')
    with open(mapping_output_path, "wb") as f:
        pickle.dump(mapping, f)
    print(f"Mapping saved to {mapping_output_path}.")

def main():
    # File paths for the updated index and mapping.
    input_csv = "JobHunter/data/jobs_with_summary.csv"   # Use your CSV that has cleaned and summarized job postings.
    index_output_path = "JobHunter/data/bert_faiss_index.idx"  # This file will be overwritten.
    mapping_output_path = "JobHunter/data/bert_faiss_mapping.pkl"  # This file will be overwritten.
    
    build_faiss_index(input_csv, index_output_path, mapping_output_path)

if __name__ == "__main__":
    main()

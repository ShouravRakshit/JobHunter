import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

def build_faiss_index(input_csv, index_output_path, mapping_output_path,
                      text_column="cleaned_description", model_name="all-MiniLM-L6-v2"):
    """
    Reads job postings from a CSV file, generates BERT-based embeddings for the text in `text_column`
    using SentenceTransformers, builds a FAISS index, and saves both the index and a mapping of metadata.
    
    Parameters:
      - input_csv (str): Path to the CSV file containing job postings.
      - index_output_path (str): Path where the FAISS index will be saved.
      - mapping_output_path (str): Path where the metadata mapping (pickle) will be saved.
      - text_column (str): Column name containing the text to embed.
      - model_name (str): Name of the SentenceTransformer model to use.
    
    Returns:
      None (the FAISS index and mapping are saved to disk).
    """
    # Load the data
    df = pd.read_csv(input_csv)
    texts = df[text_column].fillna("").tolist()
    
    # Initialize the SentenceTransformer model
    model = SentenceTransformer(model_name)
    print(f"Generating embeddings using model '{model_name}' ...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # FAISS vectorstore
    embeddings = np.array(embeddings).astype("float32")
    num_docs, d = embeddings.shape
    print(f"Generated embeddings for {num_docs} documents with dimension {d}.")
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    print(f"FAISS index built with {index.ntotal} vectors.")
    
    # save the FAISS index to disk
    faiss.write_index(index, index_output_path)
    print(f"FAISS index saved to {index_output_path}.")
    
    # Save a mapping from index (row number) to job metadata (e.g., title, cleaned_description)
    # This will allow you to know which vector corresponds to which job posting
    mapping = df[['title', text_column]].to_dict('records')
    with open(mapping_output_path, "wb") as f:
        pickle.dump(mapping, f)
    print(f"Mapping saved to {mapping_output_path}.")

def main():
    # file paths
    input_csv = "JobHunter/data/jobs_with_summary.csv"   # Contains your cleaned job descriptions.
    index_output_path = "JobHunter/data/bert_faiss_index.idx"
    mapping_output_path = "JobHunter/data/bert_faiss_mapping.pkl"
    
    build_faiss_index(input_csv, index_output_path, mapping_output_path)

if __name__ == "__main__":
    main()

from pathlib import Path
from functools import lru_cache
import faiss, pickle

ASSET_DIR = Path(__file__).resolve().parent / "ml_assets"
INDEX_FPATH = ASSET_DIR / "bert_faiss_index.idx"
MAP_FPATH   = ASSET_DIR / "bert_faiss_mapping.pkl"

@lru_cache(maxsize=1)                    # cache across warm invocations
def load_faiss():
    print(f"[DEBUG] INDEX_FPATH → {INDEX_FPATH}")
    print(f"[DEBUG] Exists? {INDEX_FPATH.exists()}")
    try:
        with INDEX_FPATH.open("rb") as f:
            print("[DEBUG] Python can open the file fine.")
    except Exception as e:
        print("[DEBUG] Python open() failed:", e)
    index = faiss.read_index(str(INDEX_FPATH))
    with MAP_FPATH.open("rb") as f:
        id2meta = pickle.load(f)
    return index, id2meta
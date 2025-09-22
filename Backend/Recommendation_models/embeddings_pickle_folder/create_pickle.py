import os
import glob
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load model
# -----------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# Input & Output folders
# -----------------------------
csv_folder = r'C:\Users\LATITUDE\Desktop\python\Intership_recommender\Backend\dataset\segregated_domains\domain_csvs'       # folder containing your CSV files
pickle_folder = "domain_pickles"  # folder to save pickle files
os.makedirs(pickle_folder, exist_ok=True)

# -----------------------------
# Process each CSV
# -----------------------------
csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

for file in csv_files:
    # Read CSV
    df = pd.read_csv(file)
    
    # Check required columns exist
    if not {"title", "description"}.issubset(df.columns):
        print(f"⚠️ Skipping {file} (missing title/description column)")
        continue
    
    # Combine title + description for embedding
    texts = (df["title"].astype(str) + " - " + df["description"].astype(str)).tolist()
    
    # Generate embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Save embeddings + original records
    data = {
        "filename": os.path.basename(file),
        "records": df.to_dict(orient="records"),
        "embeddings": embeddings
    }
    
    # Pickle filename (same as CSV but .pkl)
    pickle_file = os.path.join(
        pickle_folder,
        os.path.splitext(os.path.basename(file))[0] + ".pkl"
    )
    
    with open(pickle_file, "wb") as f:
        pickle.dump(data, f)
    
    print(f"✅ Saved {pickle_file} with {len(df)} internships")

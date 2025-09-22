import json
import pandas as pd
from pathlib import Path

# -------- Load your JSON file --------
with open(r"C:\Users\LATITUDE\Desktop\python\Intership_recommender\Backend\dataset\intership_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# -------- Create output folder --------
output_dir = Path("domain_csvs")
output_dir.mkdir(exist_ok=True)

# -------- Convert JSON to DataFrame --------
df = pd.DataFrame(data)

# -------- Split by domain and save CSV --------
for domain, group in df.groupby("domain"):
    # Replace spaces and special chars in filename
    safe_domain = domain.replace("&", "and").replace(" ", "_")
    file_path = output_dir / f"{safe_domain}.csv"
    
    group.to_csv(file_path, index=False, encoding="utf-8")
    print(f"✅ Saved {len(group)} internships to {file_path}")

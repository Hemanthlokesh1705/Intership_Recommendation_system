# -*- coding: utf-8 -*-
import os
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# -----------------------------
# Load TinyBERT model
# -----------------------------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -----------------------------
# Pickle folder
# -----------------------------
pickle_folder = r"C:\Users\LATITUDE\Desktop\python\Intership_recommender\Backend\Recommendation_models\embeddings_pickle_folder\domain_pickles"

# -----------------------------
# User input
# -----------------------------
user_skills = ['c','c++','html','css','java script','pyhton']
domain = "IT & ITeS"  # example: choose the domain
top_n = 5

# -----------------------------
# Load domain pickle
# -----------------------------
pickle_file = os.path.join(
    pickle_folder,
    domain.replace('&', 'and').replace(' ', '_') + ".pkl"
)

if not os.path.exists(pickle_file):
    raise FileNotFoundError(f"No pickle found for domain '{domain}'")

with open(pickle_file, "rb") as f:
    data = pickle.load(f)

records = data["records"]       # original CSV rows
embeddings = data["embeddings"] # precomputed embeddings

# -----------------------------
# Encode user skills
# -----------------------------
user_text = f"User profile with skills: {', '.join(user_skills)}."
user_embedding = model.encode(user_text, convert_to_tensor=True)

# -----------------------------
# Compute skill overlap function
# -----------------------------
def compute_skill_overlap(user_skills, internship_embedding, model):
    skill_sims = []
    for skill in user_skills:
        skill_embedding = model.encode(skill, convert_to_tensor=True)
        sim = util.cos_sim(skill_embedding, internship_embedding).item()
        skill_sims.append(sim)
    return sum(skill_sims) / len(skill_sims) if skill_sims else 0.0

# -----------------------------
# Compute final scores
# -----------------------------
results = []
for i, internship_embedding in enumerate(embeddings):
    sim = util.cos_sim(user_embedding, internship_embedding).item()
    overlap = compute_skill_overlap(user_skills, internship_embedding, model)
    final_score = 0.3 * sim + 0.7 * overlap

    results.append({
        "title": records[i]["title"],
        "description": records[i]["description"],
        "similarity": round(sim, 4),
        "skill_overlap": round(overlap, 4),
        "final_score": round(final_score, 4)
    })

# -----------------------------
# Sort & filter
# -----------------------------
recommendations = sorted(results, key=lambda x: x["final_score"], reverse=True)
filtered_recommendations = [r for r in recommendations if r["final_score"] > 0.10]

df = pd.DataFrame(filtered_recommendations[:top_n])
print(df[["title", "description", "similarity", "skill_overlap", "final_score"]])

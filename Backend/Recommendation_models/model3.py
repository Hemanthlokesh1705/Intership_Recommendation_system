import os
import pickle
from sentence_transformers import SentenceTransformer, util
import pandas as pd

class InternshipRecommender:
    def __init__(self, pickle_folder=r"C:\Users\LATITUDE\Desktop\python\Intership_recommender\Backend\Recommendation_models\embeddings_pickle_folder\domain_pickles", model_name="paraphrase-TinyBERT-L6-v2"):
        self.pickle_folder = pickle_folder
        self.model = SentenceTransformer(model_name)

    def load_domain_pickle(self, domain):
        """Load pickle file for a given domain"""
        filename = domain.replace('&', 'and').replace(' ', '_') + ".pkl"
        pickle_file = os.path.join(self.pickle_folder, filename)
        if not os.path.exists(pickle_file):
            raise FileNotFoundError(f"No pickle found for domain '{domain}'")
        with open(pickle_file, "rb") as f:
            data = pickle.load(f)
        return data["records"], data["embeddings"]

    def compute_skill_overlap(self, user_skills, internship_embedding):
        """Compute average cosine similarity between each user skill and internship embedding"""
        skill_sims = []
        for skill in user_skills:
            skill_emb = self.model.encode(skill, convert_to_tensor=True)
            sim = util.cos_sim(skill_emb, internship_embedding).item()
            skill_sims.append(sim)
        return sum(skill_sims) / len(skill_sims) if skill_sims else 0.0

    def recommend(self, user_skills, domain, top_n=5, min_score=0.1):
        """Return top N recommended internships for given skills and domain"""
        # Load internships for the domain
        records, embeddings = self.load_domain_pickle(domain)

        # Encode user skills as a single embedding
        user_text = f"User profile with skills: {', '.join(user_skills)}."
        user_embedding = self.model.encode(user_text, convert_to_tensor=True)

        # Compute final scores
        results = []
        for i, emb in enumerate(embeddings):
            sim = util.cos_sim(user_embedding, emb).item()
            overlap = self.compute_skill_overlap(user_skills, emb)
            final_score = 0.3 * sim + 0.7 * overlap

            # Include stipend/location if present in CSV
            rec = {
                "title": records[i].get("title", ""),
                "description": records[i].get("description", ""),
                "final_score": round(final_score, 4),
                "similarity": round(sim, 4),
                "skill_overlap": round(overlap, 4)
            }
            # Optional fields
            if "stipend" in records[i]:
                rec["stipend"] = records[i]["stipend"]
            if "location" in records[i]:
                rec["location"] = records[i]["location"]

            results.append(rec)

        # Sort & filter by minimum score
        filtered = [r for r in sorted(results, key=lambda x: x["final_score"], reverse=True) if r["final_score"] >= min_score]

        # Return top N in JSON-like dict
        return {
            "user_skills": user_skills,
            "domain": domain,
            "recommendations": filtered[:top_n]
        }

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    recommender = InternshipRecommender()
    user_skills = ["nlp", "nltk"]
    domain = "IT_and_ITeS"
    recommendations = recommender.recommend(user_skills, domain)
    import json
    print(json.dumps(recommendations, indent=2,ensure_ascii=False))

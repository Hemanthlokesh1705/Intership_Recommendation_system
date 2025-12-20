import os
import pickle
from sentence_transformers import SentenceTransformer, util

class InternshipRecommender:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.pickle_folder = r"C:\Users\LATITUDE\Desktop\python\Intership_recommender\Backend\Recommendation_models\embeddings_pickle_folder\domain_pickles"
        self.model = SentenceTransformer(model_name)

    def load_domain_pickle(self, domain):
        filename = domain.replace('&', 'and').replace(' ', '_') + ".pkl"
        pickle_file = os.path.join(self.pickle_folder, filename)

        if not os.path.exists(pickle_file):
            raise FileNotFoundError(f"No pickle found for domain '{domain}'")

        with open(pickle_file, "rb") as f:
            data = pickle.load(f)

        return data["records"], data["embeddings"]

    def compute_skill_overlap(self, user_skills, internship_embedding):
        sims = []
        for skill in user_skills:
            skill_emb = self.model.encode(skill, convert_to_tensor=True)
            sim = util.cos_sim(skill_emb, internship_embedding).item()
            sims.append(sim)
        return sum(sims) / len(sims) if sims else 0.0

    def recommend(self, user_skills, domain, top_n=5, min_score=0.1):
        records, embeddings = self.load_domain_pickle(domain)

        user_text = f"User profile with skills: {', '.join(user_skills)}"
        user_emb = self.model.encode(user_text, convert_to_tensor=True)

        results = []

        for i, emb in enumerate(embeddings):
            sim = util.cos_sim(user_emb, emb).item()
            overlap = self.compute_skill_overlap(user_skills, emb)
            score = 0.3 * sim + 0.7 * overlap

            if score < min_score:
                continue

            rec = {
                "title": records[i].get("title", ""),
                "description": records[i].get("description", ""),
                "final_score": round(score, 4),
                "similarity": round(sim, 4),
                "skill_overlap": round(overlap, 4),
                "stipend": records[i].get("stipend"),
                "location": records[i].get("location")
            }
            results.append(rec)

        results.sort(key=lambda x: x["final_score"], reverse=True)
        return results[:top_n]

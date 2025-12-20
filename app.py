from flask import Flask, request, jsonify, render_template
from recommender import InternshipRecommender

app = Flask(__name__)
recommender = InternshipRecommender()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    skills = data.get("skills")
    domain = data.get("domain")

    if not skills or not isinstance(skills, list):
        return jsonify({"error": "Skills must be a non-empty list"}), 400

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    try:
        results = recommender.recommend(skills, domain)

        return jsonify({
            "count": len(results),
            "recommendations": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

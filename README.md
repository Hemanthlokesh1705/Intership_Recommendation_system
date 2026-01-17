# Internship Recommendation System

A machine learning-based recommendation engine designed to match candidates with internships based on their specific skill sets and target domains. The system leverages semantic search and transformer models to provide high-accuracy matches.

## 🚀 Overview

This project implements a recommendation system that goes beyond simple keyword matching. By using **Sentence-BERT (S-BERT)**, the system understands the semantic context of a user's skills and compares them against internship descriptions within specific industry domains.

The architecture is built with a **Flask** backend, providing a RESTful API that accepts user profiles and returns the top-N most relevant internship opportunities, complete with similarity scores and skill-overlap metrics.

## 🛠️ Key Features

* **Semantic Matching**: Uses the `all-MiniLM-L6-v2` transformer model to encode skills and descriptions into high-dimensional vector space.
* **Domain-Specific Filtering**: Segregates data into specific industry pickles (e.g., IT & ITeS, BFSI, Healthcare) for optimized search and relevance.
* **Hybrid Scoring Engine**: Calculates a weighted final score (30% global similarity and 70% direct skill overlap) to ensure recommendations are technically grounded.
* **REST API Integration**: A Flask-based endpoint (`/recommend`) that enables easy integration with web or mobile frontends.
* **Pre-computed Embeddings**: Utilizes serialized pickle files for high-speed retrieval and low-latency responses.

## 📂 Project Structure

```text
├── Backend/
│   ├── Recommendation_models/
│   │   ├── embeddings_pickle_folder/      # Pre-computed domain embeddings
│   │   ├── model3.py                      # Core recommendation logic
│   │   └── Base_model.ipynb               # Model development and testing
│   └── dataset/
│       ├── intership_data.json            # Raw internship data
│       └── segregated_domains/            # Domain-specific datasets
├── app.py                                 # Flask application entry point
├── recommender.py                         # Recommendation class implementation
└── templates/
    └── index.html                         # Frontend interface

```

## ⚙️ Technical Workflow

1. **Data Loading**: The system identifies the target domain and loads the corresponding `.pkl` file containing internship records and their pre-computed embeddings.
2. **User Encoding**: The user's skill list is converted into a semantic embedding using `SentenceTransformer`.
3. **Scoring**:
* **Similarity**: Cosine similarity between the user profile and the internship.
* **Skill Overlap**: Individual cosine similarity checks for each specific skill against the internship embedding.


4. **Ranking**: Results are sorted by a weighted `final_score` and filtered by a minimum threshold.

## 💻 Installation & Usage

### Prerequisites

* Python 3.10+
* PyTorch
* Sentence-Transformers
* Flask

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hemanthlokesh1705/intership_recommendation_system.git

```


2. Install dependencies:
```bash
pip install flask sentence-transformers pandas

```


3. Run the application:
```bash
python app.py

```



### API Endpoint

**POST** `/recommend`

```json
{
    "skills": ["python", "machine learning", "data analysis"],
    "domain": "IT_and_ITeS"
}

```

## 📊 Model Performance

The system utilizes the `all-MiniLM-L6-v2` model, which strikes an optimal balance between performance and speed, making it suitable for real-time recommendation updates in a production environment.

---

**Author:** Hemanth Lokesh

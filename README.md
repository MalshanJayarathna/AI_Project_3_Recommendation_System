<div align="center">

# 🤖 AI Course Recommendation System

### DecodeLabs · Artificial Intelligence · Project 3

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8.0-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-3.0.3-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A content-based AI recommendation engine that matches your learning interests with the most relevant AI and tech courses — powered by TF-IDF Vectorization and Cosine Similarity.**

[🚀 Quick Start](#-quick-start) · [📖 Theory](#-theory) · [📁 Project Structure](#-project-structure) · [🌐 Web Interface](#-web-interface) · [📊 Sample Output](#-sample-output)

</div>

---

## 📌 Introduction

In today's world of online learning, thousands of courses are available — but finding the **right one** for your interests is a real challenge. This project solves that problem using **Natural Language Processing (NLP)**.

The system takes your interests as plain text, compares them with AI/tech course descriptions using mathematical text similarity, and instantly recommends the **Top 5 most relevant courses** — all without any user history, login, or ratings needed.

This project is part of the **DecodeLabs AI Project Series** and demonstrates the real-world application of content-based filtering.

---

## 🎯 Objective

> Build a **content-based recommendation system** that:
> - Accepts free-text user interests as input
> - Compares them against 20 AI/tech course descriptions using **TF-IDF Vectorization**
> - Ranks courses by **Cosine Similarity** score
> - Displays the **Top 5 most relevant courses** — via CLI and a Web UI

---

## 📚 Theory

### 🔹 Content-Based Filtering

Content-based filtering recommends items based on their **features** and a user's stated preferences — no ratings or collaborative data needed. It works great for cold-start scenarios (new users with no history).

```
User Interests  ──►  Feature Matching  ──►  Ranked Recommendations
```

---

### 🔹 TF-IDF (Term Frequency — Inverse Document Frequency)

TF-IDF converts raw text into numerical vectors, weighting each word by **how important it is** to a specific document relative to the entire corpus.

```
TF-IDF(term, document) = TF(term, document) × IDF(term)
```

| Component | Formula | Meaning |
|-----------|---------|---------|
| **TF** | count(term in doc) / total terms in doc | How often the term appears in this document |
| **IDF** | log(total docs / docs containing term) | How rare the term is across all documents |

> 💡 Common words like *"the"* or *"and"* get near-zero IDF scores and are effectively ignored. Domain words like *"neural"* or *"backpropagation"* score high.

---

### 🔹 Cosine Similarity

Cosine similarity measures the **angle** between two text vectors in high-dimensional space. It is length-independent, making it perfect for comparing documents of different sizes.

```
cosine_similarity(A, B) = (A · B) / (‖A‖ × ‖B‖)
```

| Score Range | Meaning |
|-------------|---------|
| `0.7 – 1.0` | ⭐ Excellent / very strong match |
| `0.4 – 0.7` | ✅ Good match |
| `0.1 – 0.4` | 🔶 Moderate match |
| `0.0 – 0.1` | ❌ Weak / no match |

---

### 🔹 System Workflow

```
 ┌──────────────────────────────────────────┐
 │        User enters their interests        │
 │   e.g. "python machine learning"          │
 └──────────────────┬───────────────────────┘
                    │
 ┌──────────────────▼───────────────────────┐
 │   Load items.csv (20 AI/tech courses)    │
 └──────────────────┬───────────────────────┘
                    │
 ┌──────────────────▼───────────────────────┐
 │   Build TF-IDF Matrix                    │
 │   (course descriptions → vectors)        │
 └──────────────────┬───────────────────────┘
                    │
 ┌──────────────────▼───────────────────────┐
 │   Vectorise user input                   │
 │   (same TF-IDF vocabulary)               │
 └──────────────────┬───────────────────────┘
                    │
 ┌──────────────────▼───────────────────────┐
 │   Compute Cosine Similarity              │
 │   (user vector vs. all course vectors)   │
 └──────────────────┬───────────────────────┘
                    │
 ┌──────────────────▼───────────────────────┐
 │   Rank & Return Top 5 Recommendations    │
 └──────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI_Project_3_Recommendation_System/
│
├── 📄 main.py                  ← CLI recommendation engine (run in terminal)
├── 📄 app.py                   ← Flask web server (run for web UI)
├── 📄 run_sample.py            ← Auto-runs with sample input for demo
├── 📄 requirements.txt         ← Python dependencies
├── 📄 README.md                ← Project documentation (this file)
├── 📄 .gitignore               ← Git ignore rules
│
├── 📁 data/
│   └── items.csv               ← Dataset: 20 AI/tech courses
│
├── 📁 templates/
│   └── index.html              ← Web UI HTML template (Flask)
│
├── 📁 static/
│   ├── style.css               ← Web UI stylesheet (dark glassmorphism)
│   └── script.js               ← Web UI JavaScript (API calls, rendering)
│
└── 📁 outputs/
    └── sample_output.txt       ← Auto-generated sample recommendation output
```

---

## 🚀 Quick Start

### Prerequisites

- Python **3.8 or higher**
- pip (Python package manager)
- Git (optional, for cloning)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/AI_Project_3_Recommendation_System.git
cd AI_Project_3_Recommendation_System
```

---

### Step 2 — Create a Virtual Environment *(Recommended)*

```bash
# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Run the Project

#### 🖥️ Option A: Terminal / CLI

```bash
python main.py
```

You will be prompted to enter your interests:

```
======================================================================
   DecodeLabs  |  AI Project 3  |  Course Recommendation System
======================================================================

  [1/4] Loading course dataset …        Loaded 20 courses successfully.
  [2/4] Building TF-IDF matrix …        Matrix shape: (20, 571)
  [3/4] Awaiting user input …

  Enter your interests (e.g. python machine learning automation)
  Type 'quit' to exit.

  Your interests: _
```

#### 🌐 Option B: Web Interface

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

#### ⚡ Option C: Auto Sample Run

```bash
python run_sample.py
```

Automatically runs with the query `"python ai machine learning automation"` and saves output to `outputs/sample_output.txt`.

---

## 🌐 Web Interface

The web UI features:

| Feature | Details |
|---------|---------|
| 🎨 Dark glassmorphism theme | Animated gradient orbs + floating particles |
| 🔍 Smart search box | Glowing focus ring with real-time API calls |
| ⚡ Quick chips | 6 preset interest suggestions to try instantly |
| 🏆 Ranked result cards | Gold/silver/bronze rank badges + score bars |
| 📊 Course catalogue | Browse all 20 courses in a responsive grid |
| 📱 Responsive | Works on mobile and desktop |

**REST API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the web interface |
| `POST` | `/recommend` | Returns top-5 recommendations (JSON) |
| `GET` | `/courses` | Returns all courses (JSON) |

---

## 📊 Sample Output

**Input:** `python machine learning automation`

```
======================================================================
       TOP 5 AI COURSE RECOMMENDATIONS — DecodeLabs
======================================================================

  Rank #1
  Title             : Machine Learning Fundamentals
  Category          : Machine Learning
  Similarity Score  : 0.2748
  Description       :
    Learn the core concepts of machine learning including
    supervised learning unsupervised learning regression
    classification and model evaluation using Python and scikit-learn
  --------------------------------------------------------------------

  Rank #2
  Title             : AI for Automation and Robotics
  Category          : Automation
  Similarity Score  : 0.1888
  Description       :
    Discover how artificial intelligence powers automation robotic
    process automation autonomous systems intelligent agents and
    robotic control systems in manufacturing and logistics
  --------------------------------------------------------------------

  Rank #3
  Title             : Statistics for Machine Learning
  Category          : Statistics
  Similarity Score  : 0.1353
  ...
======================================================================

  [INFO] Output saved to: outputs/sample_output.txt
```

---

## 🗄️ Dataset

The dataset (`data/items.csv`) contains **20 AI and tech courses** with three columns:

| Column | Description |
|--------|-------------|
| `title` | Full name of the course |
| `category` | Topic area (e.g. Machine Learning, NLP, Deep Learning) |
| `description` | Detailed description used for TF-IDF matching |

**Categories covered:** Machine Learning · Deep Learning · NLP · Computer Vision · Data Science · Programming · Cloud Computing · Statistics · Big Data · Automation · MLOps · Reinforcement Learning · Generative AI · AI Ethics

---

## 🔧 Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.8+ | Core programming language |
| pandas | 3.0.3 | Data loading and manipulation |
| scikit-learn | 1.8.0 | TF-IDF vectorizer and cosine similarity |
| Flask | 3.1.3 | Web server and REST API |
| HTML / CSS / JS | — | Web interface (vanilla, no frameworks) |

---

## 🧩 Key Concepts at a Glance

| Concept | What It Does |
|---------|-------------|
| **Content-Based Filtering** | Recommends based on item features, not user history |
| **TF-IDF** | Converts text to weighted numerical vectors |
| **Cosine Similarity** | Measures angular distance between two vectors |
| **Stop Word Removal** | Filters out meaningless common words |
| **N-gram Range (1, 2)** | Captures single words AND two-word phrases |

---

## 🔮 Possible Future Enhancements

- 🌐 **Deploy to cloud** — Host on Render, Railway, or Heroku for public access
- 🤝 **Collaborative filtering** — Add user ratings and preferences
- 🧠 **BERT embeddings** — Replace TF-IDF with transformer-based semantic vectors
- 📊 **Analytics dashboard** — Visualise similarity scores with charts
- 🗄️ **Database backend** — Replace CSV with PostgreSQL or MongoDB
- 🔐 **User accounts** — Save search history and favourites

---

## ✅ Conclusion

This project demonstrates how classical NLP techniques — **TF-IDF** and **Cosine Similarity** — can power a practical, explainable recommendation system with no GPU, no deep learning, and no user data required.

It is:
- ✅ **Lightweight** — runs on any machine with Python
- ✅ **Explainable** — similarity scores are transparent
- ✅ **Scalable** — works with thousands of items
- ✅ **Beginner-friendly** — every line is commented and documented
- ✅ **GitHub-ready** — clean structure, proper `.gitignore`, pinned dependencies

---

## 👨‍💻 Author

**DecodeLabs**
*Artificial Intelligence Project Series — Project 3*
*Content-Based Recommendation System*

---

<div align="center">

Built with ❤️ using **Python · Flask · pandas · scikit-learn**

⭐ *If you found this project useful, consider giving it a star on GitHub!*

</div>

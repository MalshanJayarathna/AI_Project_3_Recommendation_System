# ============================================================
# DecodeLabs AI Project 3 — AI Course Recommendation System
# ============================================================
# Author  : DecodeLabs
# Project : Content-Based AI Course Recommendation System
# Method  : TF-IDF Vectorization + Cosine Similarity
# ============================================================

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys


# ------------------------------------------------------------------
# STEP 1: Load the dataset
# ------------------------------------------------------------------
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the course dataset from a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file containing course data.

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns: title, category, description.
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] Dataset not found at: {filepath}")
        sys.exit(1)

    df = pd.read_csv(filepath)

    # Basic validation — ensure required columns exist
    required_columns = {"title", "category", "description"}
    if not required_columns.issubset(df.columns):
        print(f"[ERROR] Dataset must contain columns: {required_columns}")
        sys.exit(1)

    # Drop rows where description is missing (cannot compute similarity)
    df.dropna(subset=["description"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


# ------------------------------------------------------------------
# STEP 2: Build the TF-IDF matrix
# ------------------------------------------------------------------
def build_tfidf_matrix(descriptions: pd.Series):
    """
    Convert course descriptions into a TF-IDF feature matrix.

    TF-IDF (Term Frequency–Inverse Document Frequency) turns text into
    numerical vectors by weighting words based on how often they appear
    in a document versus across all documents. Common words like 'the'
    get low weights; domain-specific words like 'neural' get high weights.

    Parameters
    ----------
    descriptions : pd.Series
        Series of course description strings.

    Returns
    -------
    tfidf_matrix : sparse matrix
        The TF-IDF feature matrix (one row per course).
    vectorizer : TfidfVectorizer
        The fitted vectorizer (used to transform user input).
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",   # Remove common English words (the, is, and …)
        ngram_range=(1, 2),     # Consider single words AND two-word phrases
        min_df=1,               # Include terms that appear in at least 1 document
    )

    tfidf_matrix = vectorizer.fit_transform(descriptions)
    return tfidf_matrix, vectorizer


# ------------------------------------------------------------------
# STEP 3: Compute similarity between user input and all courses
# ------------------------------------------------------------------
def get_recommendations(
    user_interests: str,
    df: pd.DataFrame,
    tfidf_matrix,
    vectorizer: TfidfVectorizer,
    top_n: int = 5,
) -> pd.DataFrame:
    """
    Find the top-N courses most similar to the user's interests.

    The user's free-text interests are vectorised using the same
    TF-IDF vocabulary built from the course descriptions.  Cosine
    similarity is then computed between the user vector and every
    course vector.  Courses are ranked from highest to lowest score.

    Cosine Similarity measures the angle between two vectors in
    high-dimensional space.  A score of 1.0 means the texts are
    identical in terms of word usage; 0.0 means no overlap at all.

    Parameters
    ----------
    user_interests : str
        The user's interests entered at the terminal.
    df : pd.DataFrame
        The full course DataFrame.
    tfidf_matrix : sparse matrix
        Pre-computed TF-IDF matrix of all courses.
    vectorizer : TfidfVectorizer
        The fitted TF-IDF vectorizer.
    top_n : int
        Number of top recommendations to return.

    Returns
    -------
    pd.DataFrame
        A DataFrame of the top-N recommended courses with similarity scores.
    """
    # Transform the user's interests into a TF-IDF vector
    user_vector = vectorizer.transform([user_interests])

    # Compute cosine similarity between user vector and all course vectors
    # Result shape: (1, number_of_courses)
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Attach scores to the DataFrame
    df = df.copy()
    df["similarity_score"] = similarity_scores

    # Sort by score descending and pick the top N
    recommendations = (
        df.sort_values("similarity_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return recommendations


# ------------------------------------------------------------------
# STEP 4: Display recommendations in a formatted table
# ------------------------------------------------------------------
def display_recommendations(recommendations: pd.DataFrame) -> str:
    """
    Pretty-print the recommendation results and return them as a string.

    Parameters
    ----------
    recommendations : pd.DataFrame
        DataFrame of top-N recommended courses.

    Returns
    -------
    str
        Formatted output string (used for saving to file).
    """
    separator = "=" * 70
    lines = []

    lines.append(separator)
    lines.append("       TOP 5 AI COURSE RECOMMENDATIONS — DecodeLabs")
    lines.append(separator)

    for rank, (_, row) in enumerate(recommendations.iterrows(), start=1):
        lines.append(f"\n  Rank #{rank}")
        lines.append(f"  {'Title':<18}: {row['title']}")
        lines.append(f"  {'Category':<18}: {row['category']}")
        lines.append(f"  {'Similarity Score':<18}: {row['similarity_score']:.4f}")
        lines.append(f"  {'Description':<18}:")
        # Wrap description text at ~60 characters for readability
        desc_words = row["description"].split()
        line_buf, desc_lines = [], []
        for word in desc_words:
            line_buf.append(word)
            if len(" ".join(line_buf)) > 60:
                desc_lines.append("    " + " ".join(line_buf[:-1]))
                line_buf = [word]
        if line_buf:
            desc_lines.append("    " + " ".join(line_buf))
        lines.extend(desc_lines)
        lines.append("  " + "-" * 68)

    lines.append(separator)
    output = "\n".join(lines)
    print(output)
    return output


# ------------------------------------------------------------------
# STEP 5: Save output to file
# ------------------------------------------------------------------
def save_output(output_text: str, user_input: str, output_path: str) -> None:
    """
    Save the recommendation output to a text file.

    Parameters
    ----------
    output_text : str
        The formatted recommendation string.
    user_input : str
        The user's original interest query.
    output_path : str
        File path where output should be saved.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("DecodeLabs AI Project 3 — AI Course Recommendation System\n")
        f.write("=" * 70 + "\n")
        f.write(f"User Input   : {user_input}\n")
        f.write("=" * 70 + "\n\n")
        f.write(output_text)
        f.write("\n")

    print(f"\n  [INFO] Output saved to: {output_path}")


# ------------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------------
def main():
    """
    Main function — orchestrates data loading, vectorisation,
    similarity computation, display, and output saving.
    """
    print("\n" + "=" * 70)
    print("   DecodeLabs  |  AI Project 3  |  Course Recommendation System")
    print("=" * 70)

    # ── Resolve paths relative to this script's location ──────────
    base_dir     = os.path.dirname(os.path.abspath(__file__))
    data_path    = os.path.join(base_dir, "data", "items.csv")
    output_path  = os.path.join(base_dir, "outputs", "sample_output.txt")

    # ── Load dataset ───────────────────────────────────────────────
    print("\n  [1/4] Loading course dataset …")
    df = load_data(data_path)
    print(f"        Loaded {len(df)} courses successfully.")

    # ── Build TF-IDF matrix ────────────────────────────────────────
    print("  [2/4] Building TF-IDF matrix …")
    tfidf_matrix, vectorizer = build_tfidf_matrix(df["description"])
    print(f"        Matrix shape: {tfidf_matrix.shape}")

    # ── Get user input ─────────────────────────────────────────────
    print("  [3/4] Awaiting user input …\n")
    print("  Enter your interests / topics (e.g. python machine learning automation)")
    print("  Type 'quit' to exit.\n")

    while True:
        user_input = input("  Your interests: ").strip()

        # Handle quit command
        if user_input.lower() in ("quit", "exit", "q"):
            print("\n  Goodbye! Happy Learning with DecodeLabs!\n")
            break

        # Handle empty input
        if not user_input:
            print("  [WARNING] Input cannot be empty. Please enter your interests.\n")
            continue

        # ── Compute recommendations ────────────────────────────────
        print("\n  [4/4] Computing recommendations …")
        recommendations = get_recommendations(
            user_interests=user_input,
            df=df,
            tfidf_matrix=tfidf_matrix,
            vectorizer=vectorizer,
            top_n=5,
        )

        # Check if any meaningful matches exist
        if recommendations["similarity_score"].max() == 0:
            print("\n  [INFO] No strong matches found. Try different keywords.\n")
            continue

        # ── Display results ────────────────────────────────────────
        print()
        output_text = display_recommendations(recommendations)

        # ── Save to file ───────────────────────────────────────────
        save_output(output_text, user_input, output_path)

        # ── Ask if user wants to search again ─────────────────────
        print()
        again = input("  Search again? (yes / no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\n  Thank you for using DecodeLabs AI Recommendation System!\n")
            break
        print()


if __name__ == "__main__":
    main()

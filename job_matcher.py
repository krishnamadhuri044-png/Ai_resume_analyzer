"""
job_matcher.py
--------------
Compares the resume against a set of job roles using TF-IDF vectors
and cosine similarity, then ranks roles from highest to lowest match.
"""

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JOB_ROLES_PATH = os.path.join(_THIS_DIR, "data", "job_roles.csv")


def load_job_roles(path: str = DEFAULT_JOB_ROLES_PATH) -> pd.DataFrame:
    """Load job roles and their required skills."""
    df = pd.read_csv(path)
    df["required_skills"] = df["required_skills"].apply(
        lambda s: [skill.strip().lower() for skill in s.split(",")]
    )
    return df


def _skills_to_document(skills: list) -> str:
    """Turn a list of skills into a space-joined 'document' for vectorization."""
    return " ".join(skill.replace(" ", "_") for skill in skills)


def match_resume_to_roles(resume_skills: list, job_roles_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Calculate a match score (0-100) between the resume's extracted skills
    and each job role's required skills using TF-IDF + cosine similarity.

    Returns a DataFrame sorted by match_score descending, with columns:
    job_role, match_score, matched_skills, missing_skills
    """
    if job_roles_df is None:
        job_roles_df = load_job_roles()

    resume_doc = _skills_to_document(resume_skills)
    role_docs = [_skills_to_document(skills) for skills in job_roles_df["required_skills"]]

    documents = [resume_doc] + role_docs

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0:1]
    role_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vector, role_vectors)[0]

    results = []
    resume_skill_set = set(resume_skills)

    for idx, row in job_roles_df.reset_index(drop=True).iterrows():
        required = set(row["required_skills"])
        matched = sorted(required & resume_skill_set)
        missing = sorted(required - resume_skill_set)
        score = round(float(similarities[idx]) * 100, 1)

        results.append({
            "job_role": row["job_role"],
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
        })

    result_df = pd.DataFrame(results).sort_values(
        by="match_score", ascending=False
    ).reset_index(drop=True)

    return result_df


def recommend_top_roles(match_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Return the top N recommended roles."""
    return match_df.head(top_n)


if __name__ == "__main__":
    demo_resume_skills = ["python", "pandas", "machine learning", "scikit-learn", "sql"]
    roles = load_job_roles()
    matches = match_resume_to_roles(demo_resume_skills, roles)
    print(matches[["job_role", "match_score"]])
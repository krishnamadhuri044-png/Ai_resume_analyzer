"""
skill_extractor.py
-------------------
Extracts job-related skills from cleaned resume text using a
controlled skill dictionary (keyword matching). Skills are grouped
into categories such as programming, databases, ml, cloud, tools.
"""

import re
import pandas as pd

DEFAULT_SKILL_DICT_PATH = "data/skill_dictionary.csv"


def load_skill_dictionary(path: str = DEFAULT_SKILL_DICT_PATH) -> pd.DataFrame:
    """Load the controlled skill list with categories."""
    df = pd.read_csv(path)
    df["skill"] = df["skill"].str.strip().str.lower()
    df["category"] = df["category"].str.strip().str.lower()
    return df


def _skill_pattern(skill: str) -> re.Pattern:
    """
    Build a regex pattern for a skill that matches whole words/phrases.
    Handles special characters like '.', '+', '#' that appear in tech names
    (e.g. c++, c#, node.js) by escaping them, and still requires
    word-ish boundaries around the phrase.
    """
    escaped = re.escape(skill)
    # Use lookaround boundaries instead of \b because \b doesn't work well
    # with symbols like + and #
    pattern = r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])"
    return re.compile(pattern, flags=re.IGNORECASE)


def extract_skills(cleaned_text: str, skill_dict: pd.DataFrame = None) -> dict:
    """
    Search the cleaned resume text for known skills.

    Returns a dict: { category: [skills found in that category] }
    plus a flat 'all_skills' list.
    """
    if skill_dict is None:
        skill_dict = load_skill_dictionary()

    found_by_category = {}
    all_found = []

    for _, row in skill_dict.iterrows():
        skill = row["skill"]
        category = row["category"]
        pattern = _skill_pattern(skill)
        if pattern.search(cleaned_text):
            found_by_category.setdefault(category, [])
            if skill not in found_by_category[category]:
                found_by_category[category].append(skill)
            if skill not in all_found:
                all_found.append(skill)

    return {
        "by_category": found_by_category,
        "all_skills": sorted(all_found),
    }


if __name__ == "__main__":
    sample_text = "experienced in python, sql, pandas, machine learning, docker and c++."
    result = extract_skills(sample_text, load_skill_dictionary("data/skill_dictionary.csv"))
    print(result)

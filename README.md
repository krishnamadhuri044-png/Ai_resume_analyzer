# AI Resume Analyzer and Job Recommendation System

An NLP-based Streamlit application that analyzes a resume (PDF or DOCX),
extracts skills, compares them against job-role requirements, and
generates a match score, skill-gap report, and a simple learning roadmap.

## Features

- Upload a PDF or DOCX resume
- Automatic text extraction and cleaning
- Keyword-based skill extraction (20+ skills, grouped by category)
- TF-IDF + cosine-similarity matching against 10 job roles
- Top-3 role recommendations with match-score chart
- Skill-gap analysis for a chosen target role
- Auto-generated, week-by-week learning roadmap
- Downloadable text report

## Project Structure

```
ai_resume_analyzer/
|-- app.py                 # Streamlit dashboard (entry point)
|-- resume_parser.py       # Module 1 & 2: upload + text extraction
|-- text_cleaner.py        # Module 2: text cleaning/normalization
|-- skill_extractor.py     # Module 3: skill extraction
|-- job_matcher.py         # Module 4 & 5: TF-IDF matching + skill gap
|-- roadmap_generator.py   # Module 6: learning roadmap generation
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- data/
|   |-- job_roles.csv        # Job roles and required skills
|   |-- skill_dictionary.csv # Controlled skill list, by category
|
|-- sample_resumes/          # Sample resume(s) for testing
|-- reports/                 # Generated reports (gitignored)
|-- tests/
|   |-- test_cases.csv
```

## Setup

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. Open the local URL Streamlit prints (usually http://localhost:8501).

## Usage

1. Upload a PDF or DOCX resume.
2. Select a target job role from the dropdown.
3. Click **Analyze Resume**.
4. Review extracted skills, the match-score chart, top 3 recommended
   roles, the skill gap for your target role, and the suggested
   learning roadmap.
5. Optionally download the analysis report.

## Matching Approach (Beginner)

- Skills are detected via controlled keyword matching against
  `data/skill_dictionary.csv`.
- The resume's skill list and each job role's required-skill list are
  vectorized with **TF-IDF** and compared using **cosine similarity**
  to produce a 0-100% match score.
- The learning roadmap is rule-based: each missing skill maps to a
  short study topic (see `roadmap_generator.py`).

### Possible Advanced Upgrades

- Replace keyword matching with spaCy NER / phrase matching.
- Replace TF-IDF with Sentence Transformer embeddings for semantic matching.
- Add an LLM-generated feedback section (via Groq, Gemini, or OpenAI) with a controlled prompt.
- Add a FastAPI backend, a database (SQLite/Postgres), and Docker deployment.

## Responsible AI Notes

- This tool is for **guidance only** — it does not make hiring or
  rejection decisions.
- It does **not** score gender, age, religion, nationality, photos,
  marital status, or disability.
- Match scores are estimates based on skill/keyword overlap, not a
  measure of a candidate's true ability.
- Resumes are processed in memory for the session; no permanent
  storage is used unless explicitly added.

## Testing

See `tests/test_cases.csv` for a template to track expected vs. actual
top-role recommendations across different sample resumes.

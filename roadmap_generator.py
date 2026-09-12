"""
roadmap_generator.py
---------------------
Generates a simple, rule-based, week-by-week learning roadmap
based on the missing skills for a selected target role.
"""

# A small library of suggested learning topics/resources per skill.
# In a real project this could be expanded or loaded from a CSV/DB.
SKILL_LEARNING_NOTES = {
    "fastapi": "Learn FastAPI basics: routing, request/response models, and docs generation.",
    "docker": "Learn Docker fundamentals: images, containers, Dockerfile, and docker-compose.",
    "mlflow": "Learn MLflow for experiment tracking and model registry.",
    "cloud deployment": "Learn to deploy a model/app on AWS, Azure, or GCP (or Streamlit Cloud).",
    "power bi": "Learn Power BI basics: connecting data sources, building dashboards.",
    "sql": "Practice SQL queries: joins, aggregations, window functions.",
    "kubernetes": "Learn Kubernetes basics: pods, deployments, services.",
    "aws": "Learn core AWS services: S3, EC2, Lambda, IAM basics.",
    "azure": "Learn core Azure services: App Service, Blob Storage, Azure ML.",
    "gcp": "Learn core GCP services: Cloud Run, BigQuery, Vertex AI.",
    "transformers": "Learn the Transformers library from Hugging Face for NLP tasks.",
    "hugging face": "Explore Hugging Face Hub: models, datasets, and pipelines.",
    "sentence transformers": "Learn semantic search/embeddings with Sentence Transformers.",
    "spacy": "Learn spaCy for tokenization, NER, and dependency parsing.",
    "pytorch": "Learn PyTorch basics: tensors, autograd, building simple models.",
    "tensorflow": "Learn TensorFlow/Keras basics: building and training simple models.",
    "opencv": "Learn OpenCV basics: image processing operations.",
    "cnn": "Study Convolutional Neural Networks and build an image classifier.",
    "yolo": "Learn YOLO for real-time object detection.",
    "llm": "Learn how large language models work and how to use LLM APIs.",
    "rag": "Learn Retrieval-Augmented Generation: embeddings + vector search + LLM.",
    "langchain": "Learn LangChain for building LLM-powered applications.",
    "generative ai": "Explore generative AI concepts: prompting, fine-tuning basics.",
    "prompt engineering": "Practice writing clear, structured prompts for LLMs.",
    "react": "Learn React fundamentals: components, props, state, hooks.",
    "node.js": "Learn Node.js basics: modules, npm, building a simple API.",
    "django": "Learn Django basics: models, views, templates, ORM.",
    "flask": "Learn Flask basics: routes, templates, request handling.",
    "git": "Practice Git basics: commits, branches, merges, pull requests.",
    "github": "Learn to manage repositories, issues, and pull requests on GitHub.",
}

GENERIC_NOTE = "Study the fundamentals of {skill} through official docs and a small hands-on project."


def generate_roadmap(missing_skills: list, weeks_per_skill: int = 1) -> list:
    """
    Generate a simple rule-based roadmap.

    Returns a list of dicts: [{ "week": "Week 1", "focus": skill, "note": "..." }, ...]
    """
    roadmap = []
    week_num = 1

    for skill in missing_skills:
        note = SKILL_LEARNING_NOTES.get(skill, GENERIC_NOTE.format(skill=skill))
        roadmap.append({
            "week": f"Week {week_num}",
            "focus": skill,
            "note": note,
        })
        week_num += weeks_per_skill

    return roadmap


def format_roadmap_text(roadmap: list) -> str:
    """Format the roadmap list as readable text (for display or reports)."""
    lines = []
    for item in roadmap:
        lines.append(f"{item['week']}: {item['focus'].title()} — {item['note']}")
    return "\n".join(lines)


if __name__ == "__main__":
    missing = ["fastapi", "docker", "mlflow", "cloud deployment"]
    plan = generate_roadmap(missing)
    print(format_roadmap_text(plan))

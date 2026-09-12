import io
import pandas as pd
import streamlit as st
import plotly.express as px

from resume_parser import extract_resume_text, validate_file, UnsupportedFileTypeError
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, match_resume_to_roles, recommend_top_roles
from roadmap_generator import generate_roadmap, format_roadmap_text

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")
# ---------------------------------------------------------------------------
# Custom styling (Responsible AI tool → calm, professional, trustworthy look)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .hero {
        background: linear-gradient(135deg, #0F2C59 0%, #1B4B8A 100%);
        padding: 2.2rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        color: white;
    }
    .hero h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        margin-bottom: 0.3rem;
        color: white;
    }
    .hero p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }

    .stButton>button, .stDownloadButton>button {
        background-color: #1B4B8A;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #0F2C59;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------------------------
# Cached loaders (Responsible AI: datasets are small, verified, non-personal)
# ---------------------------------------------------------------------------
@st.cache_data
def get_skill_dictionary():
    return load_skill_dictionary("data/skill_dictionary.csv")


@st.cache_data
def get_job_roles():
    return load_job_roles("data/job_roles.csv")


skill_dict = get_skill_dictionary()
job_roles_df = get_job_roles()
all_roles = job_roles_df["job_role"].tolist()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("🧠 AI Resume Analyzer")
st.sidebar.write(
    "Upload a resume, pick a target role, and get a match score, "
    "skill-gap analysis, and a learning roadmap."
)
st.sidebar.info(
    "⚠️ **Responsible AI note:** This tool gives guidance only. "
    "It does not perform automated hiring/rejection decisions, and it "
    "does not use gender, age, religion, nationality, photo, marital "
    "status, or disability information."
)

# ---------------------------------------------------------------------------
# Module 1: Resume Upload
# ---------------------------------------------------------------------------
st.title("AI Resume Analyzer & Job Recommendation System")

col_upload, col_role = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX)", type=["pdf", "docx"]
    )

with col_role:
    target_role = st.selectbox("Select your target role", all_roles)

store_permission = st.checkbox(
    "Allow temporary storage of my resume for this session only "
    "(unchecked = processed in memory and discarded)."
)

if uploaded_file is not None:
    is_valid, message = validate_file(uploaded_file.name, uploaded_file.size)

    if not is_valid:
        st.error(message)
    else:
        st.success(f"Uploaded: {uploaded_file.name}")

        # -------------------------------------------------------------
        # Module 2: Text Extraction and Cleaning
        # -------------------------------------------------------------
        try:
            file_bytes = uploaded_file.read()
            buffer = io.BytesIO(file_bytes)
            raw_text = extract_resume_text(buffer, filename=uploaded_file.name)
        except UnsupportedFileTypeError as e:
            st.error(str(e))
            raw_text = ""
        except Exception as e:
            st.error(f"Could not read the file: {e}")
            raw_text = ""

        if raw_text:
            cleaned = clean_text(raw_text)

            # ---------------------------------------------------------
            # Module 3: Skill Extraction
            # ---------------------------------------------------------
            extraction = extract_skills(cleaned, skill_dict)
            resume_skills = extraction["all_skills"]

            st.subheader("📋 Extracted Skills")
            if resume_skills:
                for category, skills in extraction["by_category"].items():
                    st.markdown(f"**{category.title()}:** " + ", ".join(skills))
            else:
                st.warning(
                    "No known skills were detected. Try updating the resume "
                    "or expanding the skill dictionary."
                )

            # ---------------------------------------------------------
            # Module 5: Matching and Recommendation
            # ---------------------------------------------------------
            match_df = match_resume_to_roles(resume_skills, job_roles_df)

            st.subheader("📊 Match Score Overview")
            fig = px.bar(
                match_df,
                x="job_role",
                y="match_score",
                text="match_score",
                labels={"job_role": "Job Role", "match_score": "Match Score (%)"},
                title="Resume Match Score by Job Role",
            )
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            fig.update_layout(yaxis_range=[0, 100])
            st.plotly_chart(fig, width="stretch")

            top_roles = recommend_top_roles(match_df, top_n=3)
            st.subheader("🏆 Recommended Roles (Top 3)")
            st.table(top_roles[["job_role", "match_score"]].rename(
                columns={"job_role": "Job Role", "match_score": "Match Score (%)"}
            ))

            # ---------------------------------------------------------
            # Module 6: Skill-Gap Analysis (for the selected target role)
            # ---------------------------------------------------------
            st.subheader(f"🎯 Skill Gap Analysis — {target_role}")
            target_row = match_df[match_df["job_role"] == target_role].iloc[0]

            gap_col1, gap_col2 = st.columns(2)
            with gap_col1:
                st.markdown("**✅ Skills Found**")
                if target_row["matched_skills"]:
                    st.write(", ".join(target_row["matched_skills"]))
                else:
                    st.write("None found yet.")

            with gap_col2:
                st.markdown("**❌ Missing Skills**")
                if target_row["missing_skills"]:
                    st.write(", ".join(target_row["missing_skills"]))
                else:
                    st.write("No missing skills detected — great match!")

            st.metric(
                label=f"Match Score for {target_role}",
                value=f"{target_row['match_score']}%",
            )

            # ---------------------------------------------------------
            # Roadmap
            # ---------------------------------------------------------
            st.subheader("🗺️ Suggested Learning Roadmap")
            if target_row["missing_skills"]:
                roadmap = generate_roadmap(target_row["missing_skills"])
                roadmap_text = format_roadmap_text(roadmap)
                st.text(roadmap_text)
            else:
                roadmap_text = "No gaps found for this role — no roadmap needed."
                st.write(roadmap_text)

            # ---------------------------------------------------------
            # Module 7: Downloadable Report
            # ---------------------------------------------------------
            report_lines = [
                f"Target Role: {target_role}",
                f"Resume Match Score: {target_row['match_score']}%",
                "",
                "Skills Found:",
                *[f"- {s}" for s in target_row["matched_skills"]],
                "",
                "Missing Skills:",
                *[f"- {s}" for s in target_row["missing_skills"]],
                "",
                "Recommended Roles:",
                *[
                    f"{i+1}. {row['job_role']} - {row['match_score']}%"
                    for i, row in top_roles.reset_index(drop=True).iterrows()
                ],
                "",
                "Suggested Roadmap:",
                roadmap_text,
                "",
                "Note: This match score is an estimate for guidance only, "
                "not an automated hiring decision.",
            ]
            report_text = "\n".join(report_lines)

            st.download_button(
                label="⬇️ Download Analysis Report (.txt)",
                data=report_text,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
            )

            if not store_permission:
                # Responsible AI: discard resume content from session state
                del raw_text, cleaned, file_bytes
else:
    st.info("Upload a PDF or DOCX resume to get started.")

st.markdown("---")
st.caption(
    "This tool provides guidance only and does not replace human judgment "
    "in hiring decisions. Match scores are estimates based on keyword and "
    "TF-IDF similarity, not a full evaluation of ability."
)

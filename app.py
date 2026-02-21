import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pdfplumber

from agent import (
    ApplicationState,
    AgentRunner,
    ResumeAnalyzerAgent,
    JDAnalyzerAgent,
    ResumeTailorAgent,
    CoverLetterAgent,
)
from parsing import parse_resume, parse_job_description
from verification import verify_resume_match
from pdf import generate_resume_pdf, generate_cover_letter_pdf

st.set_page_config(page_title="Job Application Assistant", layout="wide")
st.title("Job Application Assistant")

# initializaing session state 
if "state" not in st.session_state:
    st.session_state.state = None

if "match_score" not in st.session_state:
    st.session_state.match_score = None

if "resume_pdf_bytes" not in st.session_state:
    st.session_state.resume_pdf_bytes = None

if "cover_pdf_bytes" not in st.session_state:
    st.session_state.cover_pdf_bytes = None

st.sidebar.header("Upload Inputs")

uploaded_resume = st.sidebar.file_uploader(
    "Upload Your Resume", type=["txt", "pdf"]
)

job_description_text = st.sidebar.text_area(
    "Paste Job Description Here", height=200
)

run_button = st.sidebar.button("Generate Tailored Documents")

# helper function to read uploaded file 
def read_uploaded_file(file) -> str:
    if file is None:
        return ""

    if file.type == "text/plain":
        return file.read().decode("utf-8")

    if file.type == "application/pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    return ""

# running the whole pipeline after user clicks the button
if run_button:
    if not uploaded_resume or not job_description_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        resume_text = read_uploaded_file(uploaded_resume)

        state = ApplicationState(
            raw_resume_text=resume_text,
            raw_job_description=job_description_text,
        )

        runner = AgentRunner(
            agents=[
                ResumeAnalyzerAgent(),
                JDAnalyzerAgent(),
                ResumeTailorAgent(),
                CoverLetterAgent(),
            ]
        )

        # Run agents
        state = runner.run(state)

        # Parse structured content
        state.resume_structured = parse_resume(resume_text)
        state.job_description_structured = parse_job_description(
            job_description_text
        )

        # Verification
        verification = verify_resume_match(
            state.tailored_resume, state.job_description_structured
        )
        state.verification = verification

        match_score = verification.get("score", 0.0) * 100

        # Generate PDFs ONCE
        resume_pdf_bytes = generate_resume_pdf(state)
        cover_pdf_bytes = generate_cover_letter_pdf(state)

        # Persist everything
        st.session_state.state = state
        st.session_state.match_score = match_score
        st.session_state.resume_pdf_bytes = resume_pdf_bytes
        st.session_state.cover_pdf_bytes = cover_pdf_bytes

# rerun safety + UI rendering
if st.session_state.state:
    state = st.session_state.state
    match_score = st.session_state.match_score

    tabs = st.tabs(["Job Keywords", "Resume", "Cover Letter"])

    # Job keywords
    with tabs[0]:
        st.subheader("Extracted Job Keywords / Phrases")
        jd_output = state.job_description_structured.get("llm_output", "")
        st.text_area(
            "Keywords / Key Concepts",
            value=jd_output,
            height=200,
        )

    # Resume
    with tabs[1]:
        st.subheader("Tailored Resume")
        st.markdown(f"**Match Score:** {match_score:.1f}%")

        resume_text = state.tailored_resume.get("llm_output", "")
        st.text_area(
            "Resume Preview",
            value=resume_text,
            height=350,
        )

        st.download_button(
            "Download Resume PDF",
            data=st.session_state.resume_pdf_bytes,
            file_name="tailored_resume.pdf",
            mime="application/pdf",
        )

    # Cover Letter
    with tabs[2]:
        st.subheader("Generated Cover Letter")

        cover_letter = state.cover_letter or ""
        st.text_area(
            "Cover Letter Preview",
            value=cover_letter,
            height=350,
        )

        st.download_button(
            "Download Cover Letter PDF",
            data=st.session_state.cover_pdf_bytes,
            file_name="cover_letter.pdf",
            mime="application/pdf",
        )
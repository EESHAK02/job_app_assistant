import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pdf import generate_resume_pdf, generate_cover_letter_pdf
from agent import ApplicationState

def test_pdf_generation(tmp_path):
    state = ApplicationState(
        tailored_resume={"llm_output": "This is a sample tailored resume."},
        cover_letter="This is a sample cover letter."
    )

    resume_path = tmp_path / "resume.pdf"
    cover_path = tmp_path / "cover_letter.pdf"

    generate_resume_pdf(state, output_path=str(resume_path))
    generate_cover_letter_pdf(state, output_path=str(cover_path))

    assert os.path.exists(resume_path)
    assert os.path.exists(cover_path)
    assert os.path.getsize(resume_path) > 0
    assert os.path.getsize(cover_path) > 0
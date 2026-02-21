from fpdf import FPDF
from typing import Optional

def generate_pdf(text: str, output_path: str, title: Optional[str] = None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    if title:
        pdf.cell(0, 10, title, align="C")
        pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.output(output_path)


def generate_resume_pdf(state, output_path="tailored_resume.pdf"):
    if not state.tailored_resume or "llm_output" not in state.tailored_resume:
        raise ValueError("Tailored resume is missing from state")
    generate_pdf(state.tailored_resume["llm_output"], output_path, title="Tailored Resume")


def generate_cover_letter_pdf(state, output_path="cover_letter.pdf"):
    if not state.cover_letter:
        raise ValueError("Cover letter is missing from state")
    generate_pdf(state.cover_letter, output_path, title="Cover Letter")
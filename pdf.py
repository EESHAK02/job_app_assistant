from fpdf import FPDF
from io import BytesIO
from typing import Optional


def generate_pdf_bytes(text: str, title: Optional[str] = None) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    left_margin = 15
    right_margin = 15
    usable_width = pdf.w - left_margin - right_margin

    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)

    if title:
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(usable_width, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(5)

    pdf.set_font("Helvetica", "", 12)

    for line in text.split("\n"):
        if line.strip():
            pdf.multi_cell(
                usable_width,
                8,
                line,
                new_x="LMARGIN",
                new_y="NEXT"
            )
        else:
            pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()


def generate_resume_pdf(state) -> bytes:
    if not state.tailored_resume or "llm_output" not in state.tailored_resume:
        raise ValueError("Tailored resume missing from state")

    return generate_pdf_bytes(
        state.tailored_resume["llm_output"],
        title="Tailored Resume"
    )


def generate_cover_letter_pdf(state) -> bytes:
    if not state.cover_letter:
        raise ValueError("Cover letter missing from state")

    return generate_pdf_bytes(
        state.cover_letter,
        title="Cover Letter"
    )
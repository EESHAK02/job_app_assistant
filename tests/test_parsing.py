import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from parsing import parse_resume, parse_job_description

def test_parse_resume():
    raw_text = "John Doe: Python, SQL"
    structured = parse_resume(raw_text)
    assert isinstance(structured, dict)
    assert "llm_output" in structured
    assert structured["llm_output"] == raw_text

def test_parse_job_description():
    raw_text = "Data Scientist: Python, ML"
    structured = parse_job_description(raw_text)
    assert isinstance(structured, dict)
    assert "llm_output" in structured
    assert structured["llm_output"] == raw_text
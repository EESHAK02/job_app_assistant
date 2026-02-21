import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from verification import verify_resume_match

def test_verify_resume_match():
    resume = {"llm_output": "Python, SQL"}
    jd = {"llm_output": "Python, ML"}
    result = verify_resume_match(resume, jd)
    assert isinstance(result, dict)
    assert result["verified"] is True
    assert result["score"] == 1.0
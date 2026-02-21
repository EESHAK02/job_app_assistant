import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm import call_llm, LLMError

def test_call_llm_basic():
    output = call_llm(
        system_prompt="You are a helpful assistant.",
        user_prompt="Say hello world in one sentence."
    )
    assert isinstance(output, str)
    assert "hello" in output.lower()
import subprocess
from typing import Optional


class LLMError(Exception):
    """Custom exception for LLM errors."""
    pass


def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: str = "llama3.1:latest",
    temperature: float = 0.3,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Calls a local Ollama model using the CLI and returns the generated text.
    Mimics the same system+user prompt style as the HTTP API version.
    """

    # Combine system and user prompts
    full_prompt = f"""SYSTEM:
{system_prompt}

USER:
{user_prompt}
"""

    # Build the CLI command
    cmd = ["ollama", "run", model, full_prompt]

    # Execute the command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise LLMError(f"Ollama subprocess failed: {e.stderr.strip()}")
    except FileNotFoundError:
        raise LLMError("Ollama CLI not found. Make sure Ollama is installed and in PATH.")

    output = result.stdout.strip()
    if not output:
        raise LLMError("Ollama returned empty output.")

    return output
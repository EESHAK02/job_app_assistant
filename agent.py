from dataclasses import dataclass, field
from typing import Dict, Any, List
from llm import call_llm


@dataclass
class ApplicationState:
    """
    Central state passed between all agents.
    """
    raw_resume_text: str = ""
    raw_job_description: str = ""

    resume_structured: Dict[str, Any] = field(default_factory=dict)
    job_description_structured: Dict[str, Any] = field(default_factory=dict)

    tailored_resume: Dict[str, Any] = field(default_factory=dict)
    cover_letter: str = ""

    verification: Dict[str, Any] = field(default_factory=dict)

    execution_log: List[str] = field(default_factory=list)
    status: str = "initialized"

#defining the agent interface 
class BaseAgent:
    name: str = "base_agent"

    def run(self, state: ApplicationState) -> ApplicationState:
        raise NotImplementedError

# definig the execution graph
class AgentRunner:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents

    def run(self, state: ApplicationState) -> ApplicationState:
        state.status = "running"

        for agent in self.agents:
            state.execution_log.append(f"Running agent: {agent.name}")
            state = agent.run(state)

        state.status = "completed"
        return state
    
#defining subagents to test first, later can replace with internal logic 

# class ResumeAnalyzerAgent(BaseAgent):
#     name = "resume_analyzer"

#     def run(self, state: ApplicationState) -> ApplicationState:
#         state.resume_structured = {"stub": True}
#         return state

class ResumeAnalyzerAgent(BaseAgent):
    name = "resume_analyzer"

    def run(self, state: ApplicationState) -> ApplicationState:
        if not state.raw_resume_text:
            state.execution_log.append("No resume text provided.")
            return state

        system_prompt = "You are an expert resume parser. Extract the resume into structured JSON with keys: name, email, phone, skills, experience, education."
        user_prompt = state.raw_resume_text

        try:
            structured_resume_text = call_llm(system_prompt, user_prompt)
            # For now, we can just store the raw LLM response.
            # Later, we can parse it to dict if needed
            state.resume_structured = {"llm_output": structured_resume_text}
            state.execution_log.append("Resume analyzed successfully.")
        except Exception as e:
            state.execution_log.append(f"Error analyzing resume: {e}")

        return state


# class JDAnalyzerAgent(BaseAgent):
#     name = "jd_analyzer"

#     def run(self, state: ApplicationState) -> ApplicationState:
#         state.job_description_structured = {"stub": True}
#         return state

class JDAnalyzerAgent(BaseAgent):
    name = "jd_analyzer"

    def run(self, state: ApplicationState) -> ApplicationState:
        if not state.raw_job_description:
            state.execution_log.append("No job description provided.")
            return state

        system_prompt = (
            "You are an expert job description analyzer. "
            "Extract the following structured information in JSON: "
            "title, required_skills, responsibilities, experience, education."
        )
        user_prompt = state.raw_job_description

        try:
            structured_jd_text = call_llm(system_prompt, user_prompt)
            # Store raw LLM output for now
            state.job_description_structured = {"llm_output": structured_jd_text}
            state.execution_log.append("Job description analyzed successfully.")
        except Exception as e:
            state.execution_log.append(f"Error analyzing job description: {e}")

        return state
    
class ResumeTailorAgent(BaseAgent):
    name = "resume_tailor"

    def run(self, state: ApplicationState) -> ApplicationState:
        if not state.resume_structured or not state.job_description_structured:
            state.execution_log.append("Cannot tailor resume: missing input data.")
            return state

        system_prompt = (
            "You are an expert resume editor. Rewrite the resume to align with "
            "the provided job description while keeping the content truthful and professional."
        )
        user_prompt = (
            f"Resume (structured): {state.resume_structured}\n"
            f"Job Description (structured): {state.job_description_structured}"
        )

        try:
            tailored_resume_text = call_llm(system_prompt, user_prompt)
            state.tailored_resume = {"llm_output": tailored_resume_text}
            state.execution_log.append("Resume tailored successfully.")
        except Exception as e:
            state.execution_log.append(f"Error tailoring resume: {e}")

        return state
    
class CoverLetterAgent(BaseAgent):
    name = "cover_letter_generator"

    def run(self, state: ApplicationState) -> ApplicationState:
        if not state.tailored_resume or not state.job_description_structured:
            state.execution_log.append("Cannot generate cover letter: missing input data.")
            return state

        system_prompt = (
            "You are an expert career coach. Write a professional cover letter that "
            "matches the provided tailored resume to the job description."
        )
        user_prompt = (
            f"Tailored Resume: {state.tailored_resume}\n"
            f"Job Description: {state.job_description_structured}"
        )

        try:
            cover_letter_text = call_llm(system_prompt, user_prompt)
            state.cover_letter = cover_letter_text
            state.execution_log.append("Cover letter generated successfully.")
        except Exception as e:
            state.execution_log.append(f"Error generating cover letter: {e}")

        return state
    

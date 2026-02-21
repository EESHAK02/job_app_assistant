import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agent import (
    ApplicationState,
    AgentRunner,
    ResumeAnalyzerAgent,
    JDAnalyzerAgent,
    ResumeTailorAgent,
    CoverLetterAgent
)


# def test_agent_execution_flow():
#     state = ApplicationState(
#         raw_resume_text="resume text",
#         raw_job_description="job description"
#     )

#     runner = AgentRunner(
#         agents=[
#             ResumeAnalyzerAgent(),
#             JDAnalyzerAgent(),
#         ]
#     )

#     final_state = runner.run(state)

#     assert final_state.status == "completed"
#     assert final_state.resume_structured != {}
#     assert final_state.job_description_structured != {}
#     #assert len(final_state.execution_log) == 2
#     assert final_state.execution_log == [
#     "Running agent: resume_analyzer",
#     "Resume analyzed successfully.",
#     "Running agent: jd_analyzer",
#     "Job description analyzed successfully."
#   ]



def test_resume_analyzer_agent():
    sample_resume = """
    John Doe
    john.doe@example.com
    +1 123-456-7890
    Skills: Python, Data Analysis
    Experience: 2 years as Data Scientist at XYZ Corp
    Education: B.Sc. in Computer Science
    """

    state = ApplicationState(raw_resume_text=sample_resume)
    agent = ResumeAnalyzerAgent()
    updated_state = agent.run(state)

    assert "llm_output" in updated_state.resume_structured
    assert len(updated_state.execution_log) > 0
    assert updated_state.execution_log[-1] == "Resume analyzed successfully."

def test_jd_analyzer_agent():
    sample_jd = """
    Data Scientist
    Required Skills: Python, SQL, Machine Learning
    Responsibilities: Analyze data, build models, communicate results
    Experience: 3+ years in data science
    Education: B.Sc. or M.Sc. in relevant field
    """

    state = ApplicationState(raw_job_description=sample_jd)
    agent = JDAnalyzerAgent()
    updated_state = agent.run(state)

    assert "llm_output" in updated_state.job_description_structured
    assert len(updated_state.execution_log) > 0
    assert updated_state.execution_log[-1] == "Job description analyzed successfully."

def test_resume_tailor_agent():
    state = ApplicationState(
        resume_structured={"llm_output": "Sample resume content"},
        job_description_structured={"llm_output": "Sample JD content"}
    )
    agent = ResumeTailorAgent()
    updated_state = agent.run(state)

    assert "llm_output" in updated_state.tailored_resume
    assert updated_state.execution_log[-1] == "Resume tailored successfully."

def test_cover_letter_agent():
    state = ApplicationState(
        tailored_resume={"llm_output": "Tailored resume text"},
        job_description_structured={"llm_output": "Sample JD content"}
    )
    agent = CoverLetterAgent()
    updated_state = agent.run(state)

    assert isinstance(updated_state.cover_letter, str)
    assert updated_state.execution_log[-1] == "Cover letter generated successfully."

def test_full_agent_flow():
    state = ApplicationState(
        raw_resume_text="John Doe resume with Python, SQL experience",
        raw_job_description="Data Scientist role requiring Python, SQL, ML"
    )

    runner = AgentRunner(
        agents=[
            ResumeAnalyzerAgent(),
            JDAnalyzerAgent(),
            ResumeTailorAgent(),
            CoverLetterAgent()
        ]
    )

    final_state = runner.run(state)

    # Status and logs
    assert final_state.status == "completed"
    assert len(final_state.execution_log) >= 4

    # Each agent produced output
    assert "llm_output" in final_state.resume_structured
    assert "llm_output" in final_state.job_description_structured
    assert "llm_output" in final_state.tailored_resume
    assert isinstance(final_state.cover_letter, str)
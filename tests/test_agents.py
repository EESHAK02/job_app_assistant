import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agent import (
    ApplicationState,
    AgentRunner,
    ResumeAnalyzerAgent,
    JDAnalyzerAgent,
)


def test_agent_execution_flow():
    state = ApplicationState(
        raw_resume_text="resume text",
        raw_job_description="job description"
    )

    runner = AgentRunner(
        agents=[
            ResumeAnalyzerAgent(),
            JDAnalyzerAgent(),
        ]
    )

    final_state = runner.run(state)

    assert final_state.status == "completed"
    assert final_state.resume_structured != {}
    assert final_state.job_description_structured != {}
    assert len(final_state.execution_log) == 2
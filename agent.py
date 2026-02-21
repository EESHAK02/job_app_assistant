from dataclasses import dataclass, field
from typing import Dict, Any, List


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

class ResumeAnalyzerAgent(BaseAgent):
    name = "resume_analyzer"

    def run(self, state: ApplicationState) -> ApplicationState:
        state.resume_structured = {"stub": True}
        return state


class JDAnalyzerAgent(BaseAgent):
    name = "jd_analyzer"

    def run(self, state: ApplicationState) -> ApplicationState:
        state.job_description_structured = {"stub": True}
        return state
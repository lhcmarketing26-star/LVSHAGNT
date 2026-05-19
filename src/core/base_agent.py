"""Base class for all LVSHAGNT agents."""
from __future__ import annotations
from abc import ABC, abstractmethod
from src.core.context import SharedContext
from src.core.types import AgentResult, TaskPayload


class BaseAgent(ABC):
    name: str = "base_agent"
    description: str = ""

    def __init__(self, context: SharedContext) -> None:
        self.context = context

    @abstractmethod
    async def run(self, payload: TaskPayload) -> AgentResult:
        """Execute the agent's primary task."""
        ...

    def __repr__(self) -> str:
        return f"<Agent: {self.name}>"

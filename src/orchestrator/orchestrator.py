"""
LVSHAGNT Orchestrator
Central coordinator that initialises all agents, manages the shared context,
and routes incoming requests to the correct agent pipeline.
"""
from __future__ import annotations
import logging
from typing import Any

from src.core.context import SharedContext
from src.core.db import Database
from src.core.llm import LLMClient
from src.core.types import AgentResult, TaskPayload
from src.agents import (
    DatabaseAgent, EnchantedAgent, LVSHGenAgent,
    LVSHOpAgent, LVSHPlanAgent,
)

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, llm_provider: str = "openai") -> None:
        self.context = SharedContext()
        self.db = Database()
        self.llm = LLMClient(provider=llm_provider)

        # Initialise all agents
        self.agents: dict[str, Any] = {
            "enchantedagent": EnchantedAgent(self.context, self.llm),
            "lvshopagent":    LVSHOpAgent(self.context),
            "lvshplanagent":  LVSHPlanAgent(self.context, self.llm),
            "lvshgenagent":   LVSHGenAgent(self.context, self.llm),
            "database_agent": DatabaseAgent(self.context, self.db),
        }
        logger.info("[Orchestrator] Initialised %d agents", len(self.agents))

    async def startup(self) -> None:
        await self.db.connect()
        logger.info("[Orchestrator] Database connected")

    async def shutdown(self) -> None:
        await self.db.disconnect()
        logger.info("[Orchestrator] Shutdown complete")

    async def handle(self, agent_name: str, payload: TaskPayload) -> AgentResult:
        """Route a payload to the specified agent."""
        agent = self.agents.get(agent_name)
        if not agent:
            return AgentResult(
                success=False,
                data=None,
                agent=agent_name,
                error=f"Agent '{agent_name}' not found. Available: {list(self.agents.keys())}",
            )
        logger.info("[Orchestrator] → %s | task: %s", agent_name, payload.get("task_type"))
        result = await agent.run(payload)
        logger.info("[Orchestrator] ← %s | success: %s", agent_name, result.success)
        return result

    async def chat(self, message: str, user_id: str = "anonymous", session_id: str = "default") -> str:
        """Convenience method — send a chat message through EnchantedAgent."""
        result = await self.handle("enchantedagent", {
            "task_type": "chat",
            "message": message,
            "user_id": user_id,
            "session_id": session_id,
        })
        return result.data.get("response", "") if result.success else result.error or "Error"

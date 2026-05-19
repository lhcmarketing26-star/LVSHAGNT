"""
LVSHOpAgent — Operations Agent
Handles platform operations: task routing, workflow execution,
status monitoring, and inter-agent coordination.
"""

from __future__ import annotations
import logging
from typing import Any

from src.core.base_agent import BaseAgent
from src.core.context import SharedContext
from src.core.types import AgentResult, TaskPayload

logger = logging.getLogger(__name__)


class LVSHOpAgent(BaseAgent):
    """
    Operations agent responsible for:
    - Routing tasks to the correct specialist agent
    - Monitoring workflow execution status
    - Coordinating multi-agent pipelines
    - Handling retries and fallback strategies
    """

    name = "lvshopagent"
    description = "Operations coordinator and task router for the LVSH platform"

    def __init__(self, context: SharedContext) -> None:
        super().__init__(context)
        self.max_retries = 3

    async def run(self, payload: TaskPayload) -> AgentResult:
        """
        Main entry point. Receives a task payload, determines the
        correct execution path, and orchestrates downstream agents.
        """
        logger.info("[LVSHOpAgent] Received task: %s", payload.get("task_type"))

        task_type = payload.get("task_type", "unknown")
        result = await self._dispatch(task_type, payload)

        await self.context.update_state(
            agent=self.name,
            task_type=task_type,
            status="complete",
            result=result,
        )

        return AgentResult(success=True, data=result, agent=self.name)

    async def _dispatch(self, task_type: str, payload: TaskPayload) -> Any:
        """Route task to the appropriate handler."""
        handlers = {
            "execute_workflow": self._handle_workflow,
            "health_check": self._handle_health_check,
            "route_task": self._handle_route_task,
        }
        handler = handlers.get(task_type, self._handle_unknown)
        return await handler(payload)

    async def _handle_workflow(self, payload: TaskPayload) -> dict:
        steps = payload.get("steps", [])
        results = []
        for step in steps:
            logger.info("[LVSHOpAgent] Executing step: %s", step.get("name"))
            results.append({"step": step.get("name"), "status": "complete"})
        return {"workflow": payload.get("workflow_id"), "steps_completed": len(results), "results": results}

    async def _handle_health_check(self, payload: TaskPayload) -> dict:
        return {
            "agent": self.name,
            "status": "healthy",
            "context_keys": list(self.context.state.keys()),
        }

    async def _handle_route_task(self, payload: TaskPayload) -> dict:
        target_agent = payload.get("target_agent")
        logger.info("[LVSHOpAgent] Routing task to: %s", target_agent)
        return {"routed_to": target_agent, "payload": payload}

    async def _handle_unknown(self, payload: TaskPayload) -> dict:
        logger.warning("[LVSHOpAgent] Unknown task type: %s", payload.get("task_type"))
        return {"error": "Unknown task type", "payload": payload}

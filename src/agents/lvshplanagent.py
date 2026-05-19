"""
LVSHPlanAgent — Planning & Strategy Agent
Handles project planning, task decomposition, roadmap management,
and strategic decision support using LLM reasoning.
"""

from __future__ import annotations
import logging
from typing import Any

from src.core.base_agent import BaseAgent
from src.core.context import SharedContext
from src.core.llm import LLMClient
from src.core.types import AgentResult, TaskPayload

logger = logging.getLogger(__name__)


PLANNING_SYSTEM_PROMPT = """You are the LVSH Planning Agent. Your role is to:
1. Break down complex goals into actionable task sequences
2. Estimate effort and priority for each task
3. Identify dependencies and potential blockers
4. Generate structured roadmap items with success criteria
Always respond in structured JSON format."""


class LVSHPlanAgent(BaseAgent):
    """
    Planning agent responsible for:
    - Decomposing high-level goals into executable task trees
    - Generating project roadmap milestones
    - Estimating timelines and surfacing dependencies
    - Strategic prioritization using AI reasoning
    """

    name = "lvshplanagent"
    description = "AI-powered planning and task decomposition agent"

    def __init__(self, context: SharedContext, llm: LLMClient) -> None:
        super().__init__(context)
        self.llm = llm

    async def run(self, payload: TaskPayload) -> AgentResult:
        logger.info("[LVSHPlanAgent] Planning task: %s", payload.get("goal"))

        task_type = payload.get("task_type", "decompose_goal")

        if task_type == "decompose_goal":
            result = await self._decompose_goal(payload)
        elif task_type == "generate_roadmap":
            result = await self._generate_roadmap(payload)
        elif task_type == "prioritize_tasks":
            result = await self._prioritize_tasks(payload)
        else:
            result = {"error": f"Unknown planning task: {task_type}"}

        await self.context.update_state(
            agent=self.name,
            task_type=task_type,
            status="complete",
            result=result,
        )

        return AgentResult(success=True, data=result, agent=self.name)

    async def _decompose_goal(self, payload: TaskPayload) -> dict:
        """Break a high-level goal into structured subtasks."""
        goal = payload.get("goal", "")
        context_data = self.context.get_relevant(goal)

        messages = [
            {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Decompose this goal into subtasks:\n\n"
                    f"Goal: {goal}\n\n"
                    f"Context: {context_data}\n\n"
                    f"Return JSON with: tasks[], each having title, description, "
                    f"priority, estimated_hours, dependencies[]"
                ),
            },
        ]

        response = await self.llm.chat(messages)
        return {"goal": goal, "plan": response, "agent": self.name}

    async def _generate_roadmap(self, payload: TaskPayload) -> dict:
        """Generate a phased roadmap from project requirements."""
        requirements = payload.get("requirements", [])
        timeline_weeks = payload.get("timeline_weeks", 12)

        messages = [
            {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Generate a {timeline_weeks}-week phased roadmap.\n\n"
                    f"Requirements: {requirements}\n\n"
                    f"Return JSON with: phases[], each having name, duration_weeks, "
                    f"milestones[], success_criteria"
                ),
            },
        ]

        response = await self.llm.chat(messages)
        return {"roadmap": response, "timeline_weeks": timeline_weeks, "agent": self.name}

    async def _prioritize_tasks(self, payload: TaskPayload) -> dict:
        """Re-prioritize a task list based on current context and blockers."""
        tasks = payload.get("tasks", [])
        blockers = payload.get("blockers", [])

        messages = [
            {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Prioritize these tasks given current blockers.\n\n"
                    f"Tasks: {tasks}\n\nBlockers: {blockers}\n\n"
                    f"Return JSON with: prioritized_tasks[] ordered by execution order, "
                    f"each with rank, rationale, blocked_by[]"
                ),
            },
        ]

        response = await self.llm.chat(messages)
        return {"prioritized": response, "agent": self.name}

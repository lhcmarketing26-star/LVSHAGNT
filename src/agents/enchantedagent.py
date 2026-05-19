"""
EnchantedAgent — Conversational Interface Agent
The primary user-facing agent. Handles natural language understanding,
conversation memory, intent classification, and response generation.
Acts as the front door to the entire LVSHAGNT platform.
"""

from __future__ import annotations
import logging
from typing import Any

from src.core.base_agent import BaseAgent
from src.core.context import SharedContext
from src.core.llm import LLMClient
from src.core.types import AgentResult, TaskPayload

logger = logging.getLogger(__name__)


ENCHANTED_SYSTEM_PROMPT = """You are the LVSH Enchanted Agent — the primary conversational
interface for the LVSH AI Platform. You are warm, sharp, and deeply capable.

Your job:
1. Understand what the user wants (intent classification)
2. Route complex tasks to specialist agents (plan, gen, ops, db)
3. Maintain conversation context across messages
4. Respond naturally while coordinating backend intelligence

Always be concise, friendly, and action-oriented. Never be robotic.
When you route a task, explain what you're doing in plain language."""


INTENT_CLASSIFICATION_PROMPT = """Classify the user's intent into one of:
- PLAN: planning, roadmapping, task decomposition, prioritization
- GENERATE: writing, coding, emails, reports, summaries
- OPERATE: workflow execution, routing, monitoring, coordination
- DATA: database queries, data sync, analytics, record management
- CONVERSE: general questions, clarifications, chitchat
- UNKNOWN: cannot classify

Return JSON: {intent, confidence, sub_intent, route_to_agent}"""


class EnchantedAgent(BaseAgent):
    """
    Conversational interface agent responsible for:
    - Natural language understanding and intent detection
    - Multi-turn conversation with persistent memory
    - Intelligent routing to specialist agents
    - Synthesizing multi-agent results into coherent responses
    - Personality and tone management
    """

    name = "enchantedagent"
    description = "Primary conversational interface — the face of the LVSH platform"

    INTENT_AGENT_MAP = {
        "PLAN": "lvshplanagent",
        "GENERATE": "lvshgenagent",
        "OPERATE": "lvshopagent",
        "DATA": "database_agent",
    }

    def __init__(self, context: SharedContext, llm: LLMClient) -> None:
        super().__init__(context)
        self.llm = llm
        self.conversation_history: list[dict] = []

    async def run(self, payload: TaskPayload) -> AgentResult:
        task_type = payload.get("task_type", "chat")
        logger.info("[EnchantedAgent] Handling: %s", task_type)

        if task_type == "chat":
            result = await self._handle_chat(payload)
        elif task_type == "classify_intent":
            result = await self._classify_intent(payload)
        elif task_type == "synthesize":
            result = await self._synthesize_results(payload)
        else:
            result = await self._handle_chat(payload)

        await self.context.update_state(
            agent=self.name, task_type=task_type, status="complete", result=result
        )
        return AgentResult(success=True, data=result, agent=self.name)

    async def _handle_chat(self, payload: TaskPayload) -> dict:
        """Process a user message: classify intent, route if needed, respond."""
        user_message = payload.get("message", "")
        user_id = payload.get("user_id", "anonymous")
        session_id = payload.get("session_id", "default")

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Classify intent
        intent_data = await self._classify_intent({"message": user_message})
        intent = intent_data.get("intent", "CONVERSE")
        route_to = intent_data.get("route_to_agent")

        # For conversational intents, respond directly
        if intent == "CONVERSE" or not route_to:
            messages = [
                {"role": "system", "content": ENCHANTED_SYSTEM_PROMPT},
                *self.conversation_history[-10:],  # Last 10 turns
            ]
            response_text = await self.llm.chat(messages)
        else:
            # Delegate and synthesize
            response_text = (
                f"I'm routing this to the {route_to} for you. "
                f"Stand by while I get the best result for: \"{user_message}\""
            )

        self.conversation_history.append({"role": "assistant", "content": response_text})

        # Persist context
        await self.context.update_state(
            agent=self.name,
            user_id=user_id,
            session_id=session_id,
            last_intent=intent,
            conversation_length=len(self.conversation_history),
        )

        return {
            "response": response_text,
            "intent": intent,
            "routed_to": route_to,
            "session_id": session_id,
            "agent": self.name,
        }

    async def _classify_intent(self, payload: TaskPayload) -> dict:
        """Determine what the user wants and which agent should handle it."""
        message = payload.get("message", "")
        messages = [
            {"role": "system", "content": INTENT_CLASSIFICATION_PROMPT},
            {"role": "user", "content": message},
        ]
        result = await self.llm.chat(messages, max_tokens=200)

        # Safe parse — fallback to CONVERSE if LLM returns non-JSON
        try:
            import json
            parsed = json.loads(result)
        except Exception:
            parsed = {"intent": "CONVERSE", "confidence": 0.5, "route_to_agent": None}

        return parsed

    async def _synthesize_results(self, payload: TaskPayload) -> dict:
        """Combine results from multiple agents into a single user-facing response."""
        results = payload.get("results", [])
        original_query = payload.get("original_query", "")

        messages = [
            {"role": "system", "content": ENCHANTED_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Original query: {original_query}\n\n"
                    f"Agent results: {results}\n\n"
                    f"Synthesize a clear, concise response for the user."
                ),
            },
        ]
        response = await self.llm.chat(messages, max_tokens=800)
        return {"synthesized_response": response, "source_results": results, "agent": self.name}

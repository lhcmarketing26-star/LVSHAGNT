"""
LVSHGenAgent — Generation Agent
Handles AI content generation: code, copy, emails, reports,
summaries, and any LLM-driven creative or analytical output.
"""

from __future__ import annotations
import logging
from typing import Any

from src.core.base_agent import BaseAgent
from src.core.context import SharedContext
from src.core.llm import LLMClient
from src.core.types import AgentResult, TaskPayload

logger = logging.getLogger(__name__)


GENERATION_SYSTEM_PROMPT = """You are the LVSH Generation Agent — an expert at producing
high-quality output: code, documentation, emails, reports, and structured content.
Always produce clean, production-ready output. No filler. No placeholders."""


class LVSHGenAgent(BaseAgent):
    """
    Generation agent responsible for:
    - Code generation and refactoring suggestions
    - Email and communication drafting
    - Report and summary generation
    - Structured document creation (JSON, Markdown, HTML)
    - Prompt-based content pipelines
    """

    name = "lvshgenagent"
    description = "LLM-powered content and code generation agent"

    def __init__(self, context: SharedContext, llm: LLMClient) -> None:
        super().__init__(context)
        self.llm = llm

    async def run(self, payload: TaskPayload) -> AgentResult:
        task_type = payload.get("task_type", "generate_text")
        logger.info("[LVSHGenAgent] Running generation task: %s", task_type)

        dispatch = {
            "generate_text": self._generate_text,
            "generate_code": self._generate_code,
            "generate_email": self._generate_email,
            "generate_report": self._generate_report,
            "summarize": self._summarize,
        }

        handler = dispatch.get(task_type)
        if not handler:
            return AgentResult(
                success=False,
                data={"error": f"Unknown task: {task_type}"},
                agent=self.name,
            )

        result = await handler(payload)
        await self.context.update_state(agent=self.name, task_type=task_type, status="complete", result=result)
        return AgentResult(success=True, data=result, agent=self.name)

    async def _generate_text(self, payload: TaskPayload) -> dict:
        prompt = payload.get("prompt", "")
        tone = payload.get("tone", "professional")
        max_tokens = payload.get("max_tokens", 1000)

        messages = [
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Tone: {tone}\n\n{prompt}"},
        ]
        output = await self.llm.chat(messages, max_tokens=max_tokens)
        return {"output": output, "type": "text", "agent": self.name}

    async def _generate_code(self, payload: TaskPayload) -> dict:
        spec = payload.get("spec", "")
        language = payload.get("language", "python")
        style_guide = payload.get("style_guide", "PEP8 / production-grade")

        messages = [
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Language: {language}\nStyle: {style_guide}\n\n"
                    f"Write production-ready code for:\n{spec}\n\n"
                    f"Include: docstrings, type hints, error handling."
                ),
            },
        ]
        output = await self.llm.chat(messages, max_tokens=2000)
        return {"output": output, "language": language, "type": "code", "agent": self.name}

    async def _generate_email(self, payload: TaskPayload) -> dict:
        subject = payload.get("subject", "")
        context_info = payload.get("context", "")
        recipient = payload.get("recipient", "")
        tone = payload.get("tone", "professional")

        messages = [
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Write a {tone} email.\n"
                    f"To: {recipient}\nSubject: {subject}\nContext: {context_info}\n\n"
                    f"Return JSON: {{subject, body, preview_text}}"
                ),
            },
        ]
        output = await self.llm.chat(messages)
        return {"email": output, "type": "email", "agent": self.name}

    async def _generate_report(self, payload: TaskPayload) -> dict:
        data = payload.get("data", {})
        report_type = payload.get("report_type", "summary")
        format_type = payload.get("format", "markdown")

        messages = [
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Generate a {report_type} report in {format_type} format.\n\n"
                    f"Data: {data}\n\n"
                    f"Include: executive summary, key findings, recommended actions."
                ),
            },
        ]
        output = await self.llm.chat(messages, max_tokens=2000)
        return {"report": output, "format": format_type, "type": "report", "agent": self.name}

    async def _summarize(self, payload: TaskPayload) -> dict:
        content = payload.get("content", "")
        max_length = payload.get("max_length", 200)
        style = payload.get("style", "bullet_points")

        messages = [
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Summarize the following in {style} format, max {max_length} words:\n\n{content}"
                ),
            },
        ]
        output = await self.llm.chat(messages, max_tokens=500)
        return {"summary": output, "style": style, "agent": self.name}

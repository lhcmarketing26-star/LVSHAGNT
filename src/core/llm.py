"""LLM client wrapper — supports OpenAI and Anthropic."""
from __future__ import annotations
import os
import logging
from typing import Any

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, provider: str = "openai", model: str | None = None) -> None:
        self.provider = provider
        self.model = model or ("gpt-4o" if provider == "openai" else "claude-3-5-sonnet-20241022")

    async def chat(self, messages: list[dict], max_tokens: int = 1000) -> str:
        if self.provider == "openai":
            return await self._openai_chat(messages, max_tokens)
        elif self.provider == "anthropic":
            return await self._anthropic_chat(messages, max_tokens)
        raise ValueError(f"Unknown provider: {self.provider}")

    async def _openai_chat(self, messages: list[dict], max_tokens: int) -> str:
        import openai
        client = openai.AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _anthropic_chat(self, messages: list[dict], max_tokens: int) -> str:
        import anthropic
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_messages = [m for m in messages if m["role"] != "system"]
        client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = await client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=user_messages,
        )
        return response.content[0].text

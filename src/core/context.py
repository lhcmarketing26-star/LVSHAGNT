"""Shared context store — cross-agent state and knowledge access."""
from __future__ import annotations
import asyncio
from typing import Any


class SharedContext:
    """Thread-safe shared state for all agents in a session."""

    def __init__(self) -> None:
        self.state: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def update_state(self, **kwargs: Any) -> None:
        async with self._lock:
            self.state.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def get_relevant(self, query: str) -> dict:
        """Return context entries relevant to the given query (simple keyword match)."""
        keywords = query.lower().split()
        return {
            k: v for k, v in self.state.items()
            if any(kw in str(k).lower() or kw in str(v).lower() for kw in keywords)
        }

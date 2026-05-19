"""Shared type definitions for LVSHAGNT."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

TaskPayload = dict[str, Any]


@dataclass
class AgentResult:
    success: bool
    data: Any
    agent: str
    error: str | None = None
    metadata: dict = field(default_factory=dict)

"""Basic smoke tests for all 5 LVSHAGNT agents."""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.core.context import SharedContext
from src.agents import LVSHOpAgent, LVSHPlanAgent, LVSHGenAgent, EnchantedAgent, DatabaseAgent


@pytest.fixture
def context():
    return SharedContext()


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.chat = AsyncMock(return_value='{"intent": "CONVERSE", "confidence": 0.9, "route_to_agent": null}')
    return llm


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.ping = AsyncMock(return_value=True)
    db.query = AsyncMock(return_value=[])
    db.insert = AsyncMock(return_value="test-id-123")
    db.update = AsyncMock(return_value=True)
    db.delete = AsyncMock(return_value=True)
    db.sync_table = AsyncMock(return_value=5)
    db.upsert = AsyncMock(return_value="upsert-id-123")
    return db


@pytest.mark.asyncio
async def test_lvshopagent_health_check(context):
    agent = LVSHOpAgent(context)
    result = await agent.run({"task_type": "health_check"})
    assert result.success
    assert result.data["status"] == "healthy"
    assert result.agent == "lvshopagent"


@pytest.mark.asyncio
async def test_lvshopagent_workflow(context):
    agent = LVSHOpAgent(context)
    result = await agent.run({
        "task_type": "execute_workflow",
        "workflow_id": "wf-001",
        "steps": [{"name": "step_1"}, {"name": "step_2"}],
    })
    assert result.success
    assert result.data["steps_completed"] == 2


@pytest.mark.asyncio
async def test_lvshplanagent_decompose(context, mock_llm):
    agent = LVSHPlanAgent(context, mock_llm)
    result = await agent.run({"task_type": "decompose_goal", "goal": "Build a REST API"})
    assert result.success
    assert result.agent == "lvshplanagent"


@pytest.mark.asyncio
async def test_lvshgenagent_text(context, mock_llm):
    mock_llm.chat = AsyncMock(return_value="Generated text output")
    agent = LVSHGenAgent(context, mock_llm)
    result = await agent.run({"task_type": "generate_text", "prompt": "Write a welcome message"})
    assert result.success
    assert result.data["type"] == "text"


@pytest.mark.asyncio
async def test_enchantedagent_chat(context, mock_llm):
    mock_llm.chat = AsyncMock(side_effect=[
        '{"intent": "CONVERSE", "confidence": 0.9, "route_to_agent": null}',
        "Hello! How can I help you today?",
    ])
    agent = EnchantedAgent(context, mock_llm)
    result = await agent.run({"task_type": "chat", "message": "Hello!", "user_id": "u1", "session_id": "s1"})
    assert result.success
    assert "response" in result.data


@pytest.mark.asyncio
async def test_database_agent_health(context, mock_db):
    agent = DatabaseAgent(context, mock_db)
    result = await agent.run({"task_type": "health_check"})
    assert result.success
    assert result.data["db_connected"] is True


@pytest.mark.asyncio
async def test_database_agent_create(context, mock_db):
    agent = DatabaseAgent(context, mock_db)
    result = await agent.run({"task_type": "create", "table": "users", "data": {"name": "Liam"}})
    assert result.success
    assert result.data["id"] == "test-id-123"

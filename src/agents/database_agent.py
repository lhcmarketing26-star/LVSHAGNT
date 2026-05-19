"""
DatabaseAgent — Data & Persistence Agent
Handles all database operations: CRUD, migrations, sync jobs,
analytics queries, and the shared knowledge store for all agents.
"""

from __future__ import annotations
import logging
from datetime import datetime, timezone
from typing import Any

from src.core.base_agent import BaseAgent
from src.core.context import SharedContext
from src.core.db import Database
from src.core.types import AgentResult, TaskPayload

logger = logging.getLogger(__name__)


class DatabaseAgent(BaseAgent):
    """
    Database agent responsible for:
    - CRUD operations on all platform entities
    - Scheduled hourly data sync jobs
    - Cross-agent shared knowledge store (read/write)
    - Analytics aggregation and reporting queries
    - Schema migrations (via Alembic)
    - Data integrity checks and self-healing
    """

    name = "database_agent"
    description = "Central data persistence and knowledge store agent"

    SYNC_INTERVAL_SECONDS = 3600  # 1 hour per README spec

    def __init__(self, context: SharedContext, db: Database) -> None:
        super().__init__(context)
        self.db = db

    async def run(self, payload: TaskPayload) -> AgentResult:
        task_type = payload.get("task_type", "query")
        logger.info("[DatabaseAgent] Task: %s", task_type)

        dispatch = {
            "query": self._handle_query,
            "create": self._handle_create,
            "update": self._handle_update,
            "delete": self._handle_delete,
            "sync": self._handle_sync,
            "knowledge_read": self._handle_knowledge_read,
            "knowledge_write": self._handle_knowledge_write,
            "health_check": self._handle_health_check,
            "analytics": self._handle_analytics,
        }

        handler = dispatch.get(task_type, self._handle_unknown)
        result = await handler(payload)

        await self.context.update_state(
            agent=self.name, task_type=task_type, status="complete", result=result
        )
        return AgentResult(success=True, data=result, agent=self.name)

    # ── CRUD ──────────────────────────────────────────────────────────────────

    async def _handle_query(self, payload: TaskPayload) -> dict:
        table = payload.get("table", "")
        filters = payload.get("filters", {})
        limit = payload.get("limit", 100)
        offset = payload.get("offset", 0)

        records = await self.db.query(table, filters=filters, limit=limit, offset=offset)
        return {
            "table": table, "count": len(records),
            "records": records, "agent": self.name
        }

    async def _handle_create(self, payload: TaskPayload) -> dict:
        table = payload.get("table", "")
        data = payload.get("data", {})
        data["created_at"] = datetime.now(timezone.utc).isoformat()

        record_id = await self.db.insert(table, data)
        logger.info("[DatabaseAgent] Created record %s in %s", record_id, table)
        return {"id": record_id, "table": table, "agent": self.name}

    async def _handle_update(self, payload: TaskPayload) -> dict:
        table = payload.get("table", "")
        record_id = payload.get("id", "")
        updates = payload.get("updates", {})
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()

        success = await self.db.update(table, record_id, updates)
        return {"id": record_id, "table": table, "updated": success, "agent": self.name}

    async def _handle_delete(self, payload: TaskPayload) -> dict:
        table = payload.get("table", "")
        record_id = payload.get("id", "")

        success = await self.db.delete(table, record_id)
        logger.info("[DatabaseAgent] Deleted %s from %s: %s", record_id, table, success)
        return {"id": record_id, "table": table, "deleted": success, "agent": self.name}

    # ── Sync ──────────────────────────────────────────────────────────────────

    async def _handle_sync(self, payload: TaskPayload) -> dict:
        """Hourly sync job — reconcile platform state with DB."""
        logger.info("[DatabaseAgent] Running hourly sync...")
        synced_tables = []
        errors = []

        tables_to_sync = payload.get("tables", ["users", "sessions", "knowledge_store", "agent_logs"])

        for table in tables_to_sync:
            try:
                count = await self.db.sync_table(table)
                synced_tables.append({"table": table, "records_synced": count})
            except Exception as e:
                errors.append({"table": table, "error": str(e)})
                logger.error("[DatabaseAgent] Sync failed for %s: %s", table, e)

        return {
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "tables_synced": len(synced_tables),
            "errors": len(errors),
            "details": synced_tables,
            "agent": self.name,
        }

    # ── Shared Knowledge Store ────────────────────────────────────────────────

    async def _handle_knowledge_read(self, payload: TaskPayload) -> dict:
        """Read from the shared knowledge store used by all agents."""
        key = payload.get("key", "")
        namespace = payload.get("namespace", "global")

        record = await self.db.query(
            "knowledge_store",
            filters={"key": key, "namespace": namespace},
            limit=1,
        )
        value = record[0].get("value") if record else None
        return {"key": key, "namespace": namespace, "value": value, "found": bool(value), "agent": self.name}

    async def _handle_knowledge_write(self, payload: TaskPayload) -> dict:
        """Write to the shared knowledge store."""
        key = payload.get("key", "")
        value = payload.get("value")
        namespace = payload.get("namespace", "global")
        ttl_hours = payload.get("ttl_hours")  # None = permanent

        data = {
            "key": key,
            "namespace": namespace,
            "value": value,
            "written_by": payload.get("source_agent", self.name),
            "expires_at": None,
        }
        if ttl_hours:
            from datetime import timedelta
            data["expires_at"] = (
                datetime.now(timezone.utc) + timedelta(hours=ttl_hours)
            ).isoformat()

        record_id = await self.db.upsert("knowledge_store", data, conflict_key=["key", "namespace"])
        logger.info("[DatabaseAgent] Knowledge written: %s/%s", namespace, key)
        return {"id": record_id, "key": key, "namespace": namespace, "agent": self.name}

    # ── Analytics ─────────────────────────────────────────────────────────────

    async def _handle_analytics(self, payload: TaskPayload) -> dict:
        """Aggregate platform usage statistics."""
        metric = payload.get("metric", "agent_activity")
        since = payload.get("since")  # ISO datetime string

        agg = await self.db.aggregate("agent_logs", metric=metric, since=since)
        return {"metric": metric, "data": agg, "agent": self.name}

    # ── Health ────────────────────────────────────────────────────────────────

    async def _handle_health_check(self, payload: TaskPayload) -> dict:
        is_connected = await self.db.ping()
        return {
            "agent": self.name,
            "db_connected": is_connected,
            "status": "healthy" if is_connected else "degraded",
        }

    async def _handle_unknown(self, payload: TaskPayload) -> dict:
        return {"error": f"Unknown task: {payload.get('task_type')}", "agent": self.name}

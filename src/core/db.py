"""Database abstraction layer — PostgreSQL via asyncpg."""
from __future__ import annotations
import os
import logging
from typing import Any

logger = logging.getLogger(__name__)


class Database:
    def __init__(self) -> None:
        self._pool = None

    async def connect(self) -> None:
        import asyncpg
        self._pool = await asyncpg.create_pool(os.environ["DATABASE_URL"], min_size=2, max_size=10)
        logger.info("[Database] Connected to PostgreSQL")

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()

    async def ping(self) -> bool:
        try:
            async with self._pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False

    async def query(self, table: str, filters: dict = {}, limit: int = 100, offset: int = 0) -> list[dict]:
        where_clause = " AND ".join(f"{k} = ${i+1}" for i, k in enumerate(filters))
        sql = f"SELECT * FROM {table}"
        if where_clause:
            sql += f" WHERE {where_clause}"
        sql += f" LIMIT {limit} OFFSET {offset}"
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(sql, *filters.values())
        return [dict(r) for r in rows]

    async def insert(self, table: str, data: dict) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(data)))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) RETURNING id"
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(sql, *data.values())
        return str(row["id"])

    async def update(self, table: str, record_id: str, updates: dict) -> bool:
        set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(updates))
        sql = f"UPDATE {table} SET {set_clause} WHERE id = ${len(updates)+1}"
        async with self._pool.acquire() as conn:
            result = await conn.execute(sql, *updates.values(), record_id)
        return result != "UPDATE 0"

    async def delete(self, table: str, record_id: str) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute(f"DELETE FROM {table} WHERE id = $1", record_id)
        return result != "DELETE 0"

    async def upsert(self, table: str, data: dict, conflict_key: list[str]) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(data)))
        conflict = ", ".join(conflict_key)
        updates = ", ".join(f"{k} = EXCLUDED.{k}" for k in data if k not in conflict_key)
        sql = (
            f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
            f"ON CONFLICT ({conflict}) DO UPDATE SET {updates} RETURNING id"
        )
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(sql, *data.values())
        return str(row["id"])

    async def sync_table(self, table: str) -> int:
        async with self._pool.acquire() as conn:
            result = await conn.fetchval(f"SELECT COUNT(*) FROM {table}")
        return int(result or 0)

    async def aggregate(self, table: str, metric: str, since: str | None = None) -> dict:
        sql = f"SELECT COUNT(*) as total, MAX(created_at) as latest FROM {table}"
        if since:
            sql += f" WHERE created_at >= '{since}'"
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(sql)
        return dict(row) if row else {}

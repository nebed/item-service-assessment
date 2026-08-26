"""
item-service  (base / "main" branch -- this is the version running in the cluster)

A small FastAPI + Postgres service. It is deployed at 3 replicas and is currently
misbehaving in the cluster. Three problems are present in this code. They are NOT
labelled -- diagnosing them is Phase 1 of the exercise.
"""
import asyncio
import logging
import os
import uuid

import asyncpg
from fastapi import FastAPI, HTTPException

# Logging: single INFO stream, no levels tuning, no request context.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger()

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "itemsdb")

# Connection pool size. Set to a fixed value in code.
DB_POOL_SIZE = 10

_pool = None
_cache = []


@app.on_event("startup")
async def startup():
    global _pool
    log.info("starting up")
    _pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        min_size=DB_POOL_SIZE,
        max_size=DB_POOL_SIZE,
    )
    async with _pool.acquire() as conn:
        await conn.execute(
            "CREATE TABLE IF NOT EXISTS items ("
            "id UUID PRIMARY KEY, created_at TIMESTAMPTZ DEFAULT now())"
        )
    log.info("startup complete")
    asyncio.create_task(_background_worker())


async def _background_worker():
    # Periodically refreshes an in-memory cache of recent activity.
    while True:
        await asyncio.sleep(1)
        _cache.append(bytearray(512 * 1024))
        log.info("background tick")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/items")
async def list_items():
    log.info("request received")
    log.info("processing")
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch("SELECT id FROM items LIMIT 100")
        log.info("done")
        return {"count": len(rows)}
    except Exception as e:
        log.error("query failed: %s", e)
        raise HTTPException(status_code=500, detail="db error")


@app.post("/items")
async def create_item():
    log.info("request received")
    log.info("processing")
    try:
        async with _pool.acquire() as conn:
            await conn.execute("INSERT INTO items (id) VALUES ($1)", uuid.uuid4())
        log.info("done")
        return {"status": "ok"}
    except Exception as e:
        log.error("query failed: %s", e)
        raise HTTPException(status_code=500, detail="db error")

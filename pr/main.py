"""
item-service  (branch: fix/stability-issues)

Attempts to fix the stability problems reported in the cluster.
See PR_DESCRIPTION.md for the author's summary of changes.
"""
import asyncio
import logging
import os
import uuid

import asyncpg
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger()

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "itemsdb")

# Fix: pool size is now configurable instead of hardcoded.
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))

# Fix: cap the cache so it can't grow forever.
CACHE_MAX_ITEMS = 1000

_pool = None
_cache = []


@app.on_event("startup")
async def startup():
    global _pool
    dsn = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Fix: log the connection target to aid debugging.
    log.info("connecting to database: %s", dsn)
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
    global _cache
    while True:
        await asyncio.sleep(1)
        _cache.append(bytearray(512 * 1024))
        # Fix: keep only the most recent CACHE_MAX_ITEMS entries.
        if len(_cache) > CACHE_MAX_ITEMS:
            _cache = _cache[-CACHE_MAX_ITEMS:]
        log.info("background tick, cache size=%s", len(_cache))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/items")
async def list_items():
    # Fix: added more logging around the request lifecycle.
    log.info("request received for list_items")
    log.info("acquiring connection")
    log.info("processing request")
    try:
        async with _pool.acquire() as conn:
            rows = await conn.fetch("SELECT id FROM items LIMIT 100")
        log.info("query returned %s rows", len(rows))
        log.info("done")
        return {"count": len(rows)}
    except Exception as e:
        log.error("query failed: %s", e)
        raise HTTPException(status_code=500, detail="db error")


@app.post("/items")
async def create_item():
    log.info("request received for create_item")
    log.info("acquiring connection")
    log.info("processing request")
    try:
        async with _pool.acquire() as conn:
            await conn.execute("INSERT INTO items (id) VALUES ($1)", uuid.uuid4())
        log.info("done")
        return {"status": "ok"}
    except Exception as e:
        log.error("query failed: %s", e)
        raise HTTPException(status_code=500, detail="db error")

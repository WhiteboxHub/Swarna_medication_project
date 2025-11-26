from fastapi import Request, HTTPException
import time

RATE_LIMIT = {}
WINDOW = 60  # 1 minute
MAX_REQ = 60

async def rate_limit_middleware(request: Request, call_next):
    now = time.time()
    key = request.client.host
    RATE_LIMIT.setdefault(key, [])
    RATE_LIMIT[key] = [t for t in RATE_LIMIT[key] if now - t < WINDOW]
    if len(RATE_LIMIT[key]) >= MAX_REQ:
        raise HTTPException(429, "Too many requests")
    RATE_LIMIT[key].append(now)
    return await call_next(request)

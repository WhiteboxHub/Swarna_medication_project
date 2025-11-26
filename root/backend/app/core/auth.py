from fastapi import Request, HTTPException

API_KEY = "local-dev-key"

async def auth_middleware(request: Request, call_next):
    key = request.headers.get("x-api-key")
    # if key != API_KEY:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    return await call_next(request)

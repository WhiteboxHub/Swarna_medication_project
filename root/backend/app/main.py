from fastapi import FastAPI
from app.core.auth import auth_middleware
from app.core.rate_limit import rate_limit_middleware
from app.api.routes import medications, schedules, doses

app = FastAPI()

app.middleware("http")(auth_middleware)
app.middleware("http")(rate_limit_middleware)

app.include_router(medications.router)
app.include_router(schedules.router)
app.include_router(doses.router)

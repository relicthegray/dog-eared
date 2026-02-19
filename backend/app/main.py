from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health, auth, intake, sources, owned

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)

origins = [settings.FRONTEND_ORIGIN]

# In dev, also allow accessing the UI via your PC's LAN IP (phone/iPad use-case)
if settings.ENV == "dev":
    origins.append("http://192.168.1.235:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(intake.router, prefix="/intake", tags=["intake"])
app.include_router(sources.router, prefix="/sources", tags=["sources"])
app.include_router(owned.router, prefix="/owned", tags=["owned"])

@app.get("/")
def root():
    return {"name": settings.APP_NAME, "status": "ok"}

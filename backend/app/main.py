from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SmartCV Advisor API",
    version="0.1.0",
)

# Cho phép frontend React/Vite gọi backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "SmartCV Advisor Backend đang hoạt động"
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok"
    }
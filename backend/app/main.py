# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .db import db

# app = FastAPI(
#     title="SmartCV Advisor API",
#     version="0.1.0",
# )
# # Cho phép frontend React/Vite gọi backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def home() -> dict[str, str]:
#     return {
#         "message": "SmartCV Advisor Backend đang hoạt động"
#     }


# @app.get("/api/health")
# def health_check() -> dict[str, str]:
#     return {
#         "status": "ok"
#     }

#############################BÊN DƯỚI LÀ ĐĂNG KHOA CẬP NHẬT VÀO LÚC 1:06PM 19/07/2026
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import db

# 1. Import các router ông vừa viết
from .routes import analysis, cv, premium

app = FastAPI(
    title="SmartCV Advisor API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Đăng ký (include) các router này vào app chính
app.include_router(analysis.router)
app.include_router(cv.router)
app.include_router(cv.career_role_router)
app.include_router(premium.router)

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

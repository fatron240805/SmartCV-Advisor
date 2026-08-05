import os
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGODB_URI = os.getenv("MONGODB_URI") or "mongodb://localhost:27017"
MONGODB_DB = os.getenv("MONGODB_DB", "smartcv")
MONGODB_SERVER_SELECTION_TIMEOUT_MS = int(os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "5000"))
MONGODB_CONNECT_TIMEOUT_MS = int(os.getenv("MONGODB_CONNECT_TIMEOUT_MS", "5000"))
MONGODB_SOCKET_TIMEOUT_MS = int(os.getenv("MONGODB_SOCKET_TIMEOUT_MS", "10000"))
MONGODB_MAX_POOL_SIZE = int(os.getenv("MONGODB_MAX_POOL_SIZE", "50"))
MONGODB_MIN_POOL_SIZE = int(os.getenv("MONGODB_MIN_POOL_SIZE", "1"))
MONGODB_WAIT_QUEUE_TIMEOUT_MS = int(os.getenv("MONGODB_WAIT_QUEUE_TIMEOUT_MS", "5000"))
MONGODB_MAX_CONNECTING = int(os.getenv("MONGODB_MAX_CONNECTING", "4"))

client = AsyncIOMotorClient(
    MONGODB_URI,
    appname="smartcv-advisor-api",
    serverSelectionTimeoutMS=MONGODB_SERVER_SELECTION_TIMEOUT_MS,
    connectTimeoutMS=MONGODB_CONNECT_TIMEOUT_MS,
    socketTimeoutMS=MONGODB_SOCKET_TIMEOUT_MS,
    maxPoolSize=MONGODB_MAX_POOL_SIZE,
    minPoolSize=MONGODB_MIN_POOL_SIZE,
    waitQueueTimeoutMS=MONGODB_WAIT_QUEUE_TIMEOUT_MS,
    maxConnecting=MONGODB_MAX_CONNECTING,
    retryReads=True,
    retryWrites=True,
)
db = client[MONGODB_DB]

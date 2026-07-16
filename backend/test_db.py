import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "smartcv")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]

async def main():
    collection = db["test_collection"]
    doc = {"name": "test-ket-noi", "value": 123}

    inserted = await collection.insert_one(doc)
    print("Inserted id:", inserted.inserted_id)

    found = await collection.find_one({"_id": inserted.inserted_id})
    print("Found document:", found)

    client.close()

asyncio.run(main())
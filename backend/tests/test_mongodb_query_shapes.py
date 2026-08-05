from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from app.routes import analysis as analysis_routes
from app.services.analysis_service import DEFAULT_ROLES, list_career_roles


class FakeCursor:
    def __init__(self, documents: list[dict]) -> None:
        self.documents = copy.deepcopy(documents)
        self.requested_length: int | None = None

    def sort(self, *_args, **_kwargs):
        return self

    async def to_list(self, length: int | None = None) -> list[dict]:
        self.requested_length = length
        return copy.deepcopy(self.documents if length is None else self.documents[:length])


class FakeCollection:
    def __init__(self, documents: list[dict] | None = None) -> None:
        self.documents = documents or []
        self.find_calls: list[dict] = []
        self.aggregate_calls: list[list[dict]] = []
        self.last_cursor: FakeCursor | None = None

    def find(self, query: dict, *_args, **_kwargs) -> FakeCursor:
        self.find_calls.append(copy.deepcopy(query))
        self.last_cursor = FakeCursor(self.documents)
        return self.last_cursor

    def aggregate(self, pipeline: list[dict]) -> FakeCursor:
        self.aggregate_calls.append(copy.deepcopy(pipeline))
        self.last_cursor = FakeCursor(self.documents)
        return self.last_cursor


class FakeDb(dict[str, FakeCollection]):
    def __getitem__(self, name: str) -> FakeCollection:
        if name not in self:
            self[name] = FakeCollection()
        return super().__getitem__(name)


class MongoQueryShapeTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_role_summary_does_not_load_skill_collections(self) -> None:
        default_role = DEFAULT_ROLES[0]
        db = FakeDb(
            {
                "NGANHNGHIET": FakeCollection(
                    [
                        {
                            "_id": default_role["role_id"],
                            "TenNganh": default_role["name"],
                            "MoTa": default_role["description"],
                            "TrangThai": "active",
                        }
                    ]
                )
            }
        )

        roles = await list_career_roles(db, include_skills=False)

        self.assertTrue(any(role["role_id"] == default_role["role_id"] for role in roles))
        self.assertNotIn("NGANHNGHE_KYNANG", db)
        self.assertNotIn("KYNANG", db)
        self.assertNotIn("DIEMDANHGIA", db)

    async def test_full_role_list_bulk_loads_each_skill_collection_once(self) -> None:
        default_role = DEFAULT_ROLES[0]
        role_id = default_role["role_id"]
        db = FakeDb(
            {
                "NGANHNGHIET": FakeCollection(
                    [{"_id": role_id, "TenNganh": default_role["name"], "TrangThai": "active"}]
                ),
                "NGANHNGHE_KYNANG": FakeCollection(
                    [{"_id": "REL_1", "MaNganh": role_id, "MaKyNang": "SKILL_1", "TrangThai": "active"}]
                ),
                "KYNANG": FakeCollection(
                    [{"_id": "SKILL_1", "TenKyNang": "Python", "NhomKyNang": "Backend"}]
                ),
                "DIEMDANHGIA": FakeCollection(
                    [{"_id": "SCORE_1", "MaNganh": role_id, "MaKyNang": "SKILL_1", "Diem": 80, "TrongSo": 100, "MucDoQuanTrong": 3, "TrangThai": "active"}]
                ),
            }
        )

        await list_career_roles(db)

        self.assertEqual(len(db["NGANHNGHIET"].find_calls), 1)
        self.assertEqual(len(db["NGANHNGHE_KYNANG"].find_calls), 1)
        self.assertEqual(len(db["KYNANG"].find_calls), 1)
        self.assertEqual(len(db["DIEMDANHGIA"].find_calls), 1)

    async def test_history_filters_and_limits_before_lookups(self) -> None:
        history_collection = FakeCollection(
            [
                {
                    "analysis_id": "KQ_1",
                    "cv_id": "CV_1",
                    "cv_name": "cv.pdf",
                    "overall_score": 80,
                    "classification": "Tốt",
                    "role_id": "ROLE_1",
                    "role_name": "Backend",
                    "created_at": "2026-08-05T00:00:00Z",
                    "status": "completed",
                }
            ]
        )
        db = FakeDb({"LICHSUPTCV": history_collection})

        with patch.object(analysis_routes, "db", db):
            response = await analysis_routes.get_analysis_history(
                user={"user_id": "KH_1", "current_plan": "free"},
                limit=10,
            )

        pipeline = history_collection.aggregate_calls[0]
        self.assertEqual(pipeline[0], {"$match": {"MaKH": "KH_1", "MaKQ": {"$exists": True}}})
        self.assertEqual(pipeline[1], {"$sort": {"NgayPT": -1}})
        self.assertEqual(pipeline[2], {"$limit": 10})
        self.assertEqual(history_collection.last_cursor.requested_length, 10)
        self.assertEqual(response["data"][0]["analysis_id"], "KQ_1")


if __name__ == "__main__":
    unittest.main()

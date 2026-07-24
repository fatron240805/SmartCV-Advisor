"""Load and normalize the IT role skill-score dataset."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path
from typing import Any


DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "it_role_skill_score_dataset.json"


def stable_key(value: str, *, max_length: int = 56) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    tokens = re.findall(r"[A-Za-z0-9]+", ascii_text.upper())
    slug = "_".join(tokens)[:max_length].strip("_") or "ITEM"
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8].upper()
    return f"{slug}_{digest}"


def clamp_importance(value: Any) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(3, score))


def icon_label_for_role(role_name: str) -> str:
    aliases = {
        "AI / Machine Learning Engineer": "AI",
        "DataOps / MLOps": "ML",
        "UI/UX Designer": "UX",
        "QA/QC Engineer": "QA",
    }
    if role_name in aliases:
        return aliases[role_name]

    words = re.findall(r"[A-Za-z0-9]+", role_name)
    if not words:
        return "IT"
    if len(words) == 1:
        return words[0][:2].upper()
    return "".join(word[0] for word in words[:2]).upper()


def load_raw_role_dataset() -> dict[str, Any]:
    with DATASET_PATH.open("r", encoding="utf-8") as dataset_file:
        return json.load(dataset_file)


def flatten_skill_scores(skill_scores: dict[str, Any]) -> list[dict[str, Any]]:
    skills: list[dict[str, Any]] = []
    for group_name, group_scores in skill_scores.items():
        if not isinstance(group_scores, dict):
            continue
        for skill_name, score in group_scores.items():
            skills.append(
                {
                    "skill": str(skill_name),
                    "group": str(group_name),
                    "importance": clamp_importance(score),
                }
            )
    return skills


def load_default_roles() -> list[dict[str, Any]]:
    dataset = load_raw_role_dataset()
    roles: list[dict[str, Any]] = []
    for item in dataset.get("roles", []):
        role_id = str(item.get("id", "")).strip()
        role_name = str(item.get("role", "")).strip()
        if not role_id or not role_name:
            continue

        roles.append(
            {
                "role_id": role_id,
                "name": role_name,
                "description": str(item.get("description", "")).strip(),
                "status": "active",
                "skills": flatten_skill_scores(item.get("skill_scores", {})),
                "icon_label": icon_label_for_role(role_name),
                "roadmap": str(item.get("roadmap", "")).strip(),
                "dataset_version": str(dataset.get("metadata", {}).get("version", "1.0")),
            }
        )
    return roles


def score_label(score: int) -> str:
    labels = {
        0: "Không cần có",
        1: "Nice to have",
        2: "Quan trọng",
        3: "Rất quan trọng / bắt buộc",
    }
    return labels.get(score, "Không cần có")


def build_role_seed_documents(now: Any) -> dict[str, list[dict[str, Any]]]:
    roles = load_default_roles()
    skills_by_name: OrderedDict[str, dict[str, Any]] = OrderedDict()
    relations: list[dict[str, Any]] = []
    max_score_by_skill_id: dict[str, int] = {}

    role_documents: list[dict[str, Any]] = []
    for role in roles:
        role_id = role["role_id"]
        role_documents.append(
            {
                "_id": role_id,
                "TenNganh": role["name"],
                "TenNganhNormalized": role["name"].lower(),
                "MoTa": role["description"],
                "Roadmap": role["roadmap"],
                "IconLabel": role["icon_label"],
                "DatasetVersion": role["dataset_version"],
                "NgayTao": now,
                "NgayCapNhat": now,
                "TrangThai": "hoat dong",
            }
        )

        for skill in role["skills"]:
            skill_name = skill["skill"]
            skill_key = skill_name.casefold()
            if skill_key not in skills_by_name:
                skill_id = f"KN_{stable_key(skill_name)}"
                skills_by_name[skill_key] = {
                    "_id": skill_id,
                    "TenKyNang": skill_name,
                    "TenKyNangNormalized": skill_key,
                    "NhomKyNang": skill["group"],
                    "MoTa": f"Kỹ năng thuộc nhóm {skill['group']}.",
                    "NgayTao": now,
                    "NgayCapNhat": now,
                    "TrangThai": "hoat dong",
                }

            skill_doc = skills_by_name[skill_key]
            importance = int(skill["importance"])
            max_score_by_skill_id[skill_doc["_id"]] = max(max_score_by_skill_id.get(skill_doc["_id"], 0), importance)
            relations.append(
                {
                    "_id": f"NNKN_{stable_key(role_id + '_' + skill_doc['_id'])}",
                    "MaNganh": role_id,
                    "MaKyNang": skill_doc["_id"],
                    "NhomKyNang": skill["group"],
                    "Diem": float(importance),
                    "TrongSo": float(importance * 10),
                    "MucDo": score_label(importance),
                    "NgayCapNhat": now,
                }
            )

    score_documents = [
        {
            "_id": f"DDG_{skill_id.removeprefix('KN_')}",
            "MaKyNang": skill_id,
            "Diem": float(score),
            "TrongSo": float(score * 10),
            "MucDo": score_label(score),
            "NgayCapNhat": now,
        }
        for skill_id, score in max_score_by_skill_id.items()
    ]

    return {
        "roles": role_documents,
        "skills": list(skills_by_name.values()),
        "role_skills": relations,
        "skill_scores": score_documents,
    }

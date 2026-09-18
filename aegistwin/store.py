from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import AnalysisReport


class ReportStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, created_at TEXT DEFAULT CURRENT_TIMESTAMP, payload TEXT NOT NULL)"
        )
        self.connection.commit()

    def save(self, report: AnalysisReport) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO reports(id, payload) VALUES (?, ?)",
            (report.analysis_id, report.model_dump_json()),
        )
        self.connection.commit()

    def recent(self, limit: int = 10) -> list[dict]:
        rows = self.connection.execute(
            "SELECT payload FROM reports ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [json.loads(row[0]) for row in rows]


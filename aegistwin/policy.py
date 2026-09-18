from __future__ import annotations

from pathlib import Path

import yaml

from .models import SecurityPromise


def load_promises(path: Path) -> list[SecurityPromise]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("promises"), list):
        raise ValueError("Policy file must contain a 'promises' list")
    promises = [SecurityPromise.model_validate(item) for item in raw["promises"]]
    ids = [promise.id for promise in promises]
    if len(ids) != len(set(ids)):
        raise ValueError("Security promise IDs must be unique")
    return promises


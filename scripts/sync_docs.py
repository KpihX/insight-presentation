from __future__ import annotations

import os
import shutil
from pathlib import Path


DOC_MAP = {
    "README.md": "README.md",
    "CHANGELOG.md": "CHANGELOG.md",
    "TODO.md": "TODO.md",
    "frontend/README.md": "frontend/README.md",
    "backend/README.md": "backend/README.md",
    "backend/n8n/README.md": "backend/n8n/README.md",
    "backend/n8n/architecture.md": "backend/n8n/architecture.md",
    "backend/n8n/api.md": "backend/n8n/api.md",
    "backend/n8n/schema_db.md": "backend/n8n/schema_db.md",
    "backend/n8n/source.md": "backend/n8n/source.md",
    "backend/n8n/internal.md": "backend/n8n/internal.md",
    "backend/n8n/workflows/README.md": "backend/n8n/workflows/README.md",
    "backend/n8n/workflows/ingestion-v1.md": "backend/n8n/workflows/ingestion-v1.md",
    "backend/n8n/workflows/read-api-v1.md": "backend/n8n/workflows/read-api-v1.md",
    "backend/n8n/workflows/action-api-v1.md": "backend/n8n/workflows/action-api-v1.md",
    "backend/n8n/workflows/demo-seed-v1.md": "backend/n8n/workflows/demo-seed-v1.md",
}


def copy_file(source_root: Path, destination_root: Path, source_rel: str, destination_rel: str) -> None:
    source = source_root / source_rel
    destination = destination_root / destination_rel

    if not source.exists():
        raise FileNotFoundError(f"Missing source document: {source}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.is_symlink() or destination.exists():
        destination.unlink()

    shutil.copy2(source, destination)


def main() -> None:
    presentation_root = Path(__file__).resolve().parents[1]
    source_root = Path(os.environ.get("INSIGHT_SOURCE_ROOT", presentation_root.parent)).resolve()

    for source_rel, destination_rel in DOC_MAP.items():
        copy_file(source_root, presentation_root, source_rel, destination_rel)


if __name__ == "__main__":
    main()

from __future__ import annotations

import shutil
from pathlib import Path


SKIP_PARTS = {".git", ".github", "scripts", "site", "__pycache__"}
SKIP_FILES = {".gitignore"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts) or path.name in SKIP_FILES


def copy_tree(presentation_root: Path, output_root: Path) -> None:
    for candidate in presentation_root.rglob("*"):
        rel_path = candidate.relative_to(presentation_root)

        if rel_path == Path(".") or should_skip(rel_path):
            continue

        destination = output_root / rel_path

        if candidate.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate, destination)


def main() -> None:
    presentation_root = Path(__file__).resolve().parents[1]
    output_root = presentation_root / "site"

    if output_root.exists():
        shutil.rmtree(output_root)

    output_root.mkdir(parents=True, exist_ok=True)
    copy_tree(presentation_root, output_root)


if __name__ == "__main__":
    main()

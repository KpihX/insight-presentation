from __future__ import annotations

import os
import shutil
from pathlib import Path


SKIP_PARTS = {".git", ".github", "scripts", "site", "__pycache__"}
SKIP_FILES = {".gitignore"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts) or path.name in SKIP_FILES


def copy_tree(presentation_root: Path, source_root: Path, output_root: Path) -> None:
    for candidate in presentation_root.rglob("*"):
        rel_path = candidate.relative_to(presentation_root)

        if rel_path == Path(".") or should_skip(rel_path):
            continue

        destination = output_root / rel_path

        if candidate.is_dir() and not candidate.is_symlink():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)

        if candidate.is_symlink():
            target = os.readlink(candidate)
            simulated_local_path = (source_root / "presentation" / rel_path).parent / target
            source_file = simulated_local_path.resolve()

            if not source_file.exists():
                raise FileNotFoundError(
                    f"Broken presentation symlink for {rel_path}: "
                    f"{target} -> {source_file}"
                )

            shutil.copy2(source_file, destination)
            continue

        if candidate.is_file():
            shutil.copy2(candidate, destination)


def main() -> None:
    presentation_root = Path(__file__).resolve().parents[1]
    source_root = Path(os.environ.get("INSIGHT_SOURCE_ROOT", presentation_root.parent)).resolve()
    output_root = presentation_root / "site"

    if output_root.exists():
      shutil.rmtree(output_root)

    output_root.mkdir(parents=True, exist_ok=True)
    copy_tree(presentation_root, source_root, output_root)


if __name__ == "__main__":
    main()

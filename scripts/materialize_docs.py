from __future__ import annotations

import re
import shutil
from pathlib import Path


SKIP_PARTS = {".git", ".github", "scripts", "site", "__pycache__"}
SKIP_FILES = {".gitignore"}
MARKDOWN_LINK_PATTERN = re.compile(r"(?P<prefix>\[[^\]]+\]\()(?P<target>[^)]+)(?P<suffix>\))")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts) or path.name in SKIP_FILES


def normalize_markdown_target(current_dir: Path, target: str) -> str:
    parts: list[str] = list(current_dir.parts)

    for part in Path(target).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)

    return "/" + "/".join(parts)


def rewrite_markdown_links(content: str, rel_path: Path) -> str:
    current_dir = rel_path.parent

    def replace(match: re.Match[str]) -> str:
        target = match.group("target").strip()

        if (
            target.startswith("http://")
            or target.startswith("https://")
            or target.startswith("#")
            or target.startswith("mailto:")
            or target.startswith("/")
        ):
            return match.group(0)

        if not (target.endswith(".md") or target.endswith("/")):
            return match.group(0)

        absolute_target = normalize_markdown_target(current_dir, target)
        return f"{match.group('prefix')}{absolute_target}{match.group('suffix')}"

    return MARKDOWN_LINK_PATTERN.sub(replace, content)


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

        if candidate.suffix == ".md":
            rewritten = rewrite_markdown_links(candidate.read_text(), rel_path)
            destination.write_text(rewritten)
            shutil.copystat(candidate, destination)
            continue

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

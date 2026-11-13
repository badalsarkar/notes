#!/usr/bin/env python3
"""Check that a module card (MODULE.md) is complete, accurate and free of code-level detail.

Checks:
  1. Required frontmatter fields are present and not empty.
  2. Names in the frontmatter (APIs, topics, packages, tables, flags) appear somewhere in the
     repository other than in module cards.
  3. The body contains no line-number references or fenced code excerpts, and deep file paths
     are reported as warnings.
  4. The card is not longer than the line limit.

Usage:
  python3 validate_module_card.py path/to/MODULE.md --root path/to/repo [--max-lines 150]

Exit code 0 means no errors. Warnings do not change the exit code.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = ("id", "name", "archetypes", "owner", "status", "sections", "source_commit")
# Frontmatter fields whose values are names that must exist in the code. A ``None`` sub-key
# means the field itself is the list of names.
NAME_FIELDS = (
    ("provides", "apis"),
    ("provides", "topics"),
    ("provides", "packages"),
    ("consumes", "topics"),
    ("data_owned", None),
    ("flags", None),
)
SKIPPED_DIRS = (".git", ".venv", "build", "dist", "node_modules", "target", "vendor")
LINE_REFERENCE = re.compile(r"\b[\w./-]+\.\w{1,5}:\d+\b")
DEEP_PATH = re.compile(r"\b(?:src|lib|app|main|test)/[\w./-]+/[\w./-]+\.\w{1,5}\b")


def main() -> int:
    """Validate one module card and print its errors and warnings.

    Returns:
        ``1`` if the card has errors, otherwise ``0``.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("card", type=Path)
    parser.add_argument("--root", type=Path, default=Path())
    parser.add_argument("--max-lines", type=int, default=150)
    args = parser.parse_args()

    if not args.card.is_file():
        print(f"ERROR: Module card not found: {args.card}. Expected a path to a MODULE.md file.")
        return 1

    text = args.card.read_text(encoding="utf-8")
    errors, warnings = validate_card_text(text, root=args.root, max_lines=args.max_lines)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"{args.card}: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


def validate_card_text(text: str, *, root: Path, max_lines: int) -> tuple[list[str], list[str]]:
    """Return the errors and warnings found in the text of a module card.

    Args:
        text: The full content of the card, including frontmatter.
        root: The repository root searched for names referenced by the card.
        max_lines: The line count above which the card is reported as too long.

    Returns:
        A pair of lists: errors, then warnings.
    """
    frontmatter_text, body = _split_frontmatter_from_body(text)
    if frontmatter_text is None:
        return ["The card has no YAML frontmatter between '---' lines."], []

    frontmatter, fully_parsed = _parse_frontmatter(frontmatter_text)
    errors = _find_missing_required_fields(frontmatter, fully_parsed=fully_parsed)
    warnings: list[str] = []
    if fully_parsed:
        errors += _find_names_absent_from_code(frontmatter, root=root)
    else:
        warnings.append("PyYAML is not installed, so names in the frontmatter were not checked.")

    body_errors, body_warnings = _find_code_level_detail(body)
    errors += body_errors
    warnings += body_warnings

    line_count = len(text.splitlines())
    if line_count > max_lines:
        warnings.append(f"Card has {line_count} lines, above the limit of {max_lines}.")
    proposed_count = body.count("(proposed)")
    if proposed_count:
        warnings.append(f"{proposed_count} body item(s) are still marked (proposed).")
    return errors, warnings


def _split_frontmatter_from_body(text: str) -> tuple[str | None, str]:
    """Separate the YAML frontmatter from the Markdown body.

    The frontmatter starts at the first line and ends at the next line beginning with
    ``---``. Later ``---`` lines in the body, such as horizontal rules, are left in the body.
    """
    if not text.startswith("---"):
        return None, text
    head, separator, rest = text[3:].partition("\n---")
    if not separator:
        return None, text
    _, _, body = rest.partition("\n")
    return head, body


def _parse_frontmatter(frontmatter_text: str) -> tuple[dict[str, Any], bool]:
    """Parse the frontmatter, falling back to key detection when PyYAML is unavailable.

    Returns:
        The parsed mapping, and ``True`` if it was fully parsed rather than only scanned for
        top-level keys.
    """
    try:
        import yaml  # noqa: PLC0415 - optional dependency, imported only when needed
    except ImportError:
        keys = re.findall(r"^([A-Za-z_]+):", frontmatter_text, re.MULTILINE)
        return dict.fromkeys(keys), False
    return yaml.safe_load(frontmatter_text) or {}, True


def _find_missing_required_fields(frontmatter: dict[str, Any], *, fully_parsed: bool) -> list[str]:
    """Return an error for each required field that is absent, or empty when values are known."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")
        elif fully_parsed and frontmatter[field] in (None, "", []):
            errors.append(f"Required field is empty: {field}")
    return errors


def _find_names_absent_from_code(frontmatter: dict[str, Any], *, root: Path) -> list[str]:
    """Return an error for each referenced name that cannot be found in the repository."""
    errors = []
    for field, sub_field in NAME_FIELDS:
        names = frontmatter.get(field)
        if sub_field is not None:
            names = names.get(sub_field) if isinstance(names, dict) else None
        label = f"{field}.{sub_field}" if sub_field else field
        for name in names or []:
            name = str(name).strip()
            if name and not _is_name_present_in_code(name, root=root):
                errors.append(f"Name not found in repository: {label} -> {name}")
    return errors


def _is_name_present_in_code(name: str, *, root: Path) -> bool:
    """Return ``True`` if the name appears in any file under ``root`` other than module cards.

    Uses ripgrep when available because it respects ``.gitignore``; otherwise uses grep with
    the common build and dependency directories excluded.
    """
    if shutil.which("rg"):
        command = ["rg", "-q", "-F", "-g", "!**/MODULE.md", "--", name, str(root)]
    else:
        excluded = [f"--exclude-dir={directory}" for directory in SKIPPED_DIRS]
        command = ["grep", "-rqF", "--exclude=MODULE.md", *excluded, "--", name, str(root)]
    # The command is built from a fixed argument list with no shell, so the name cannot inject.
    result = subprocess.run(command, capture_output=True, check=False)  # noqa: S603
    return result.returncode == 0


def _find_code_level_detail(body: str) -> tuple[list[str], list[str]]:
    """Return errors for line references and code blocks, and warnings for deep file paths."""
    errors, warnings = [], []
    for number, line in enumerate(body.splitlines(), 1):
        if LINE_REFERENCE.search(line):
            errors.append(f"Body line {number}: line-number reference found: {line.strip()}")
        if DEEP_PATH.search(line):
            warnings.append(
                f"Body line {number}: deep file path found; prefer a type or module name: "
                f"{line.strip()}"
            )
    if "```" in body:
        errors.append("Body contains a fenced code block; module cards must not contain code.")
    return errors, warnings


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate every skill under skills/. Standard library only.

Checks the Agent Skills format plus the Journalit rules in CONTRIBUTING.md.
Reviewers still read every skill: this catches mistakes, not bad intent.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_SKILL_BYTES = 64 * 1024
ALLOWED_SUFFIXES = {".md", ".png", ".jpg", ".jpeg", ".webp"}
TIERS = {"official", "community"}

# Tool names the Journalit MCP server exposes (core skill contract 3.7.0).
JOURNALIT_TOOLS = {
    "inspect_journal", "inspect_configuration", "query_trades",
    "evaluate_trades", "analyze_behavior", "get_premarket_brief",
    "get_trade", "get_review", "view_image", "navigate_journalit",
    "describe_actions", "apply_changes", "run_integration",
    "read_skill", "list_docs", "grep_docs", "read_doc", "report_feedback",
}

# Phrases no skill should contain, whatever the context.
FORBIDDEN = [
    (re.compile(r"auto[- ]?approve", re.I), "must not auto-approve in-app approvals"),
    (re.compile(r"skip(ping)? (the )?preview", re.I), "must not skip previews"),
    (re.compile(r"retry (after|if) .{0,20}den(y|ied)", re.I), "must not retry after a denial"),
    (re.compile(r"(curl|wget|npx|pip install|npm install)\b", re.I), "must not run or install code"),
    (re.compile(r"guarantee[sd]? (profit|returns)", re.I), "must not promise profit"),
]

def parse_frontmatter(text):
    """Parse the small YAML subset skills use: top-level scalars and one
    level of nested scalars (metadata). Returns (fields, body) or raises."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with '---' frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter is not closed with '---'")
    fields, parent = {}, None
    for number, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        nested = line.startswith("  ")
        key, sep, value = line.strip().partition(":")
        if not sep:
            raise ValueError(f"frontmatter line {number} is not 'key: value'")
        value = value.strip().strip('"').strip("'")
        if nested:
            if parent is None:
                raise ValueError(f"frontmatter line {number} is indented without a parent")
            fields[parent][key] = value
        elif value == "":
            parent = key
            fields[key] = {}
        else:
            parent = None
            fields[key] = value
    return fields, text[end + 5:]


def check_skill(folder):
    errors = []
    skill_file = folder / "SKILL.md"
    if not skill_file.is_file():
        return [f"{folder.name}: missing SKILL.md"]

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() not in ALLOWED_SUFFIXES:
            errors.append(f"{path.relative_to(ROOT)}: only Markdown and images are allowed")
        if path.is_symlink():
            errors.append(f"{path.relative_to(ROOT)}: symlinks are not allowed")

    raw = skill_file.read_bytes()
    if len(raw) > MAX_SKILL_BYTES:
        errors.append(f"{folder.name}: SKILL.md is over {MAX_SKILL_BYTES} bytes")
    text = raw.decode("utf-8")
    try:
        fields, body = parse_frontmatter(text)
    except ValueError as error:
        return errors + [f"{folder.name}: {error}"]

    name = fields.get("name", "")
    if name != folder.name:
        errors.append(f"{folder.name}: name '{name}' must match the folder name")
    if not NAME_PATTERN.match(name) or len(name) > MAX_NAME:
        errors.append(f"{folder.name}: name must be lowercase-hyphenated, max {MAX_NAME} chars")
    description = fields.get("description", "")
    if not description or len(description.encode()) > MAX_DESCRIPTION:
        errors.append(f"{folder.name}: description is required, max {MAX_DESCRIPTION} bytes")

    metadata = fields.get("metadata")
    if not isinstance(metadata, dict):
        return errors + [f"{folder.name}: metadata block is required"]
    for key in ("author", "tier", "version", "journalit-tools", "writes"):
        if not metadata.get(key):
            errors.append(f"{folder.name}: metadata.{key} is required")
    if metadata.get("tier") and metadata["tier"] not in TIERS:
        errors.append(f"{folder.name}: metadata.tier must be one of {sorted(TIERS)}")

    declared = set(metadata.get("journalit-tools", "").split())
    unknown = declared - JOURNALIT_TOOLS
    if unknown:
        errors.append(f"{folder.name}: unknown Journalit tools {sorted(unknown)}")
    used = {tool for tool in JOURNALIT_TOOLS if re.search(rf"`{tool}`", body)}
    undeclared = used - declared - {"read_skill"}
    if undeclared:
        errors.append(f"{folder.name}: body uses tools not in metadata.journalit-tools: {sorted(undeclared)}")

    if "read_skill" not in body:
        errors.append(f"{folder.name}: must tell the agent to read the core skill with read_skill first")

    writes = metadata.get("writes")
    if writes not in ("true", "false"):
        errors.append(f"{folder.name}: metadata.writes must be \"true\" or \"false\"")
    uses_writes = "apply_changes" in declared or "`apply_changes`" in body
    if uses_writes and writes != "true":
        errors.append(f"{folder.name}: uses apply_changes, so metadata.writes must be \"true\"")
    if writes == "true":
        if "preview" not in body.lower():
            errors.append(f"{folder.name}: writing skills must preview changes first")

    for path in folder.rglob("*.md"):
        content = path.read_text("utf-8")
        for pattern, reason in FORBIDDEN:
            if pattern.search(content):
                errors.append(f"{path.relative_to(ROOT)}: {reason} (matched '{pattern.search(content).group(0)}')")
    return errors


def main():
    folders = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not folders:
        print("no skills found")
        return 1
    errors = [error for folder in folders for error in check_skill(folder)]
    stray = [path.name for path in SKILLS.iterdir() if path.is_file()]
    errors += [f"skills/{name}: files must live inside a skill folder" for name in stray]
    for error in errors:
        print(f"error: {error}")
    print(f"{len(folders)} skills checked, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

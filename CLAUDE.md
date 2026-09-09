# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal technical **knowledge base**, not a software project. ~95 topic-per-file Markdown notes at
the repo root (e.g. `spring-security.md`, `kafka.md`, `ai-security.md`), plus generated diagram assets.
There is no build, lint, test, or dependency tooling — do not look for or invent any. "Working in this
repo" means reading, writing, and cross-linking Markdown.

## Note conventions (match these when editing or adding notes)

- **One topic per file**, kebab-case filename = the topic (`oauth-authorization-code-grant.md`).
- **Nested bullets**, not prose paragraphs. Notes are structured as outlines: a heading, then
  indented bullets drilling down (`what` / `how` / `why` sub-nodes are common). Study a sibling file
  before writing and mirror its depth and structure.
- **Write every bullet as a plain, full sentence.** Do not use sentence fragments, telegraphic
  shorthand, or dramatic phrasing (nothing is "dead", "revolutionary", "a game changer", or "the
  loudest trend"). State facts calmly, and name the limitation alongside the benefit when describing
  an option. This applies to new notes and to any edit of an existing one.
- **Inline links** to primary sources (official docs, source code, papers) live directly on the bullet
  they support.
- **Cross-link related notes** with relative Markdown links, e.g. `[oauth.md](oauth.md)`.
- **`## Resources`** section at the end of a note collects books/courses/links for the topic.
- Some notes carry YAML frontmatter `mindmap-plugin: basic` (12 of them) — this marks the file for
  rendering by the Obsidian Mind Map plugin. Preserve it; the outline structure IS the mind map.

## Diagram workflow (mindmap/ and plantuml/)

Some topics have a companion visual diagram. The pipeline is:

- `plantuml/<topic>.txt` — the **PlantUML source** (`@startmindmap … @endmindmap`). This is the file
  to **edit** when changing a diagram.
- `mindmap/<topic>.png` — the **rendered image**, generated from the PlantUML source.
- `mindmap/<topic>.cmapx` / `test.cmapx` — image-map metadata emitted alongside the render.

Filenames are the join key: `plantuml/kubernetes.txt` → `mindmap/kubernetes.png` → often a
`kubernetes.md` note. When asked to update a diagram, edit the `.txt` source; regenerating the `.png`
requires PlantUML (Graphviz), which is not configured in-repo.

`images/` holds standalone screenshots/figures embedded in notes (not part of the PlantUML pipeline).

## Git

Commits are single notes or small edits; history uses short messages like "added note" / "notes added".
Keep commits scoped to the note(s) touched. Commit only when the user asks.

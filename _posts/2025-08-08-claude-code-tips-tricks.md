---
layout: post
title: Claude Code Tips & Tricks
date: 2025-08-08 09:47 +0000
categories: [Tips & Tricks]
tags: [AI, tools]
comments: false
excerpt: Practical ways to get more out of Claude Code in your IDE and the Claude app.
---

Claude Code can feel like a senior pair-programmer when you give it the right context and constraints. Here are compact, battle-tested tips to get more reliable results—whether you use the Claude app (Artifacts) or the VS Code extension.

## Setup & Context

### Prime with the right context
- **Anchor the project**: keep a short `ARCHITECTURE.md` (components, data flow, constraints) and a **task-specific brief** (goal, acceptance criteria, non-goals). Share or attach both before asking for changes.
- **Point to exact files**: reference paths like `app/services/user.ts` and paste the minimal surrounding code needed. Big diffs reduce precision.

### Keep CLAUDE.md up to date
- Always generate a `CLAUDE.md` (like Cursor rules). In Claude, run `/init` to scaffold it, then tailor to your repo.
- Keep it current as conventions, commands, or constraints change.
- Store drafts/screens in `images/screenshots/` and reference them when discussing UI.

## Planning & Workflow

### Ask for a plan first
- Use Plan mode (Shift‑Tab): "Propose a 3–6 step plan. Wait for confirmation."
- Benefits: surfaces hidden work, catches risks early, and lets you narrow scope before touching code.

### Constrain edits to diffs
- Say: "Return a unified diff touching only `X` and `Y`. Do not change any other files."
- Review the diff, then apply locally. Small, surgical edits = fewer regressions.

### Keep changes small and reviewable
- Ask Claude to split work into **atomic commits** with messages.
- Prefer "Phase 1: tests + types," "Phase 2: implementation," "Phase 3: cleanup/docs."

### Use Git as checkpoints
- **Claude IDE** (desktop app) has "Restore Checkpoint"
- **Claude Code** (VS Code extension) doesn't - use Git commits as your restore mechanism
- Commit after each accepted feature or diff; revert/discard when needed
- You can instruct Claude to commit after each feature when operating on your repo

## Code Quality

### Drive development with tests
- Ask for: "Write failing tests first, then minimal code to pass."
- For legacy code: "Add characterization tests around current behavior, then refactor." This preserves behavior while improving design.

### Make it reason, not guess
- Nudge with: "Explain trade‑offs briefly before coding," or "List 2–3 options, pick one, justify."
- For nontrivial changes, request a short risk checklist (perf, security, migrations, API breaks).

### Safer refactors
- Guardrails to include:
  - "Preserve public API; note any breaking changes explicitly."
  - "Do not change runtime behavior without tests that prove safety."
  - "Flag potential edge cases and add tests for them."

## Advanced Techniques

### Trace code across the repo
- Prompt patterns:
  - "Given `POST /api/users`, trace request → controller → domain → DB. Cite files and lines."
  - "Where are roles/permissions enforced before this handler runs?"
- This is great for onboarding, audits, or untangling data flows.

### Use Artifacts (Claude app) or scratch files (IDE)
- Have Claude build UI snippets, config files, or docs in an isolated "artifact/scratch" first. Iterate there, then promote to real files once stable.

### Screenshots workflow
- Drag screenshots into Claude Code to ground UI discussions.
- Keep draft ideas in `images/screenshots/`.

### Web search and Subagents
- Use Claude's web search agent; paste links to docs; Google when helpful.
- Ask Claude to break the problem down and use Subagents in parallel for faster coverage.

### When to escalate to deeper thinking
- For complex tasks, ask Claude to "think step‑by‑step," or "consider 2 alternatives and pick one." You'll get slower but more deliberate output.

## Quick Reference

### Handy prompt snippets

**General pairing prompt:**
```text
You are my coding pair. Goal: <one sentence>.
Constraints: return a small diff; don't touch unrelated files; add/adjust tests.
Plan first in <=5 steps, then wait.
```

**Refactoring with constraints:**
```text
Refactor `services/billing.ts` to remove duplication.
– Keep public API stable
– Add characterization tests first
– Return a unified diff only for files you touch
```

**Test-driven approach:**
```text
Write table-driven tests for `parseDuration()` covering malformed inputs, large values, and locale quirks. Keep tests fast and deterministic.
```

### Review everything
- Ask it to double‑check findings and diffs.
- Review generated code like a teammate's PR; don't auto‑accept.

### Final checklist for reliable outputs
- Attach minimal, relevant code context.
- Ask for a plan → review → approve.
- Demand diffs and tests.
- Run the suite locally; iterate on failures.
- Plan mode first (Shift‑Tab).
- Keep `CLAUDE.md` updated (`/init` on new projects).
- Commit often; use Git as your restore checkpoints.
- Leverage web search and Subagents where appropriate.
- Review everything; double‑check before applying.

With tight prompts and small, test‑backed diffs, Claude Code becomes a fast, dependable assistant for everyday engineering work.

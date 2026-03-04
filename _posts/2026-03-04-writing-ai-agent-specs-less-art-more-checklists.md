---
layout: post
title: 'Writing AI Agent Specs: Less Art, more checklists'
date: 2026-03-04 06:51 +0000
categories: [Tips & Tricks]
tags: [AI]
comments: false
excerpt: "How building 8 specialized AI agents for a full SDLC taught me that good specs aren't about prose — they're about checklists, boundaries, and templates."
---

I recently built a project I called **5level** (inspired by [this video](https://www.youtube.com/watch?v=bDcgHzCBgmQ)) — a framework of 8 specialized AI agents covering a full Agile SDLC: product manager, product lead, architect, tech lead, scrum master, developer, QA tester, and release lead.

**Level 4 — Developer as Product Manager** — is the idea that you write strong specifications and outcome criteria, AI implements and tests, and you evaluate results rather than every line. The primary gain is a shift from coding effort to product and system thinking. 5level covers roughly 80% of that in practice (so far March 2026). The risk — as I learned firsthand — is exactly what this post is about: **weak specs produce wrong-but-plausible results**.

Each agent is defined in a single Markdown file called `SKILL.md`. Each one has a specific role, a set of inputs and outputs, a numbered workflow, a Definition of Done checklist, and a set of rules.

Writing those 8 spec files taught me something I didn't expect: **the quality of an AI agent is almost entirely determined by the quality of its spec**. Not the model. Not the tools. The spec.

And most specs I've seen — including early versions of mine — fail for the same reason: they're written like prose. Like a job description. Like a README no one will read.

Let me show you what actually works.

---

## The Challenge

A [GitHub study](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/) of over 2,500 agent configuration files found the most common failure mode: **too vague**. Things like "write clean code" or "follow best practices" or "make sure tests pass." These aren't instructions — they're hopes.

When you hand an AI agent a vague spec, you don't get a bad result. You get a _plausible-looking_ result. The agent fills in the gaps with its own assumptions, and those assumptions compound across multiple steps until you have something that works in demos and falls apart on edge cases.

The antidote isn't more prose. It's structure.

---

## The Anatomy of a SKILL.md

Each agent in the 5level project follows the same template. Here's the skeleton:

```
---
name: sdlc-qa-tester
description: '...trigger keywords...'
compatibility: Designed for Claude Code (claude-sonnet-4-6)
metadata:
  author: pbrodner
  version: "1.2"
  sdlc-level: "4"
  role: qa-tester
---

## Role Summary       ← what this agent owns
## Inputs             ← what it receives (from whom)
## Outputs            ← what it produces (artifacts, not conversations)
## Workflow           ← numbered steps with commands and templates
## Definition of Done ← checkbox list (not prose)
## Rules              ← what it always/never does
## Collaboration Map  ← who to contact for what
```

Every section is mandatory. Remove any one of them and the agent starts guessing.

The section easiest to underspecify is **Outputs**. Not "write a test plan" — but what the test plan _is_, what file it goes to, and what downstream agent consumes it. Here's the QA agent's output list:

```
- Test Strategy Document (per Feature — requires human approval before execution)
- Test Plan (per story)
- Test Cases (per story AC scenario)
- Test Execution results
- Defect reports (Jira Bug issues)
- Test Report (PASS/FAIL summary for DoD gate)
- Traceability matrix (AC → test case → result)
```

Artifacts, not conversations. This distinction matters — an agent that "helps with QA" and an agent that "produces a traceability matrix consumed by sdlc-release-lead for release validation" are two very different things.

---

## The Workflow: 8 Agents, 3 Human Gates

The 8 agents in 5level form a pipeline. Here's how they connect:

```
Human Idea
    │
    ▼
[Product Manager] ──► Epic + Features
    │
    ▼
[Product Lead] ──────► User Stories + AC
    │
    ▼
[Architect] ─────────► SDD / ADRs
    │
    ▼
[Tech Lead] ─────────► Estimates + Technical Tasks
    │
    ▼
[QA Tester] ─────────► Test Strategy ◄── HUMAN GATE #1
    │                                    (approval required before dev)
    ▼
[Scrum Master] ──────► Sprint Entry Gate
    │
    ├─────────────────────────┐
    ▼                         ▼
[Developer]             [QA Tester]
Feature Branch          Test Cases (parallel)
    │                         │
    └───────────┬─────────────┘
                ▼
            PR Review
         [Tech Lead] ◄── HUMAN GATE #2 (high-complexity or security changes)
                │
                ▼
           QA Execution
                │
                ▼
      [Scrum Master] DoD Gate
                │
                ▼
     [Release Lead] ◄── HUMAN GATE #3 (Sprint Review + Release Gate)
                │
                ▼
            Deploy
```

Three human touchpoints. Everything else is agent-driven. This only works if each agent's spec is precise enough that it doesn't need supervision on every step.

---

## The Six Non-Negotiables

[Addy Osmani writes](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents) that good agent specs must cover six areas. I'll show you how 5level handles each one.

| Area | What It Means | How 5level Does It |
|---|---|---|
| **Commands** | Exact executable commands with flags | Each workflow step includes runnable commands: `uv run pytest -v`, `git checkout main && git pull origin main` |
| **Testing** | Framework, file locations, coverage threshold | Developer agent: "Achieve the coverage threshold set by `sdlc-architect` (default: 80% line coverage)" |
| **Project structure** | Where artifacts live | All agents write to explicit paths: `docs/backlog.md`, `docs/sdd.md`, `docs/test-strategy-[FEATURE-ID].md` |
| **Code style** | Real examples beat descriptions | Commit format is defined by example, not description (see below) |
| **Git workflow** | Branch naming, commit format, PR requirements | Developer agent has a dedicated step for each: create branch, commit format, self-review, open PR |
| **Boundaries** | What the agent must never do | Rules section in every SKILL.md — hard stops, not suggestions |

For code style, here's how the developer agent defines commit format — with an actual example, not a description:

```
[STORY-ID] imperative verb phrase describing what changed

- What was changed and why (1–3 bullets)
- AC: [AC scenario name this satisfies]
```

```
PROJ-42 Generate cryptographically secure password reset token

- Add generate_reset_token() to AuthService with 64-byte entropy
- Token expires after 1 hour per security standard ADR-007
- AC: "User requests password reset — happy path"
```

An AI agent reading this knows exactly what a commit message should look like. No interpretation needed.

---

## Three-Tier Guardrails

Every SKILL.md in 5level has a **Rules** section. But not all rules are equal. Effective rules follow a three-tier structure:

**✅ Always do** — actions the agent can take autonomously without asking:
- "Test planning starts at task definition, not code completion."
- "Every test case must trace to an AC. No AC traceability = invalid test case."
- "File bugs immediately. Do not batch defects until the end."

**⚠️ Ask first** — situations that require a human or another agent before proceeding:
- "If anything is ambiguous: post a question on the Jira story, tag `sdlc-tech-lead` or `sdlc-product-lead`, and wait for a response. **Do not implement on assumptions.**"
- "Do not execute tests until [Test Strategy] approval is recorded."

**🚫 Never do** — hard stops:
- "Never push directly to `main`."
- "Do not commit: credentials, API keys, or `.env` files."
- "Never disable, skip, or comment out a failing test."
- "Do not merge before approval."

The difference between a good spec and a dangerous one often comes down to how explicit the "never" list is. Agents are very good at finding technically-compliant ways to get things done — including ways you didn't intend. A hard stop is the only reliable prevention.

---

## Definition of Done as a Checklist

The single highest-value addition you can make to any agent spec is a **Definition of Done** with checkboxes. Not a paragraph about quality. A list the agent can verify against before declaring work complete.

Here's the QA agent's DoD:

```markdown
- [ ] All AC scenarios have at least one executed test case
- [ ] All test cases marked PASS, or defects are filed for FAILs
- [ ] All Critical and High severity bugs are resolved and re-tested with PASS
- [ ] E2E browser tests PASS (or N/A documented — story touches no UI)
- [ ] Traceability matrix is complete (every AC → test case → result)
- [ ] Test Report issued to `sdlc-scrum-master`
```

And the developer's:

```markdown
- [ ] Feature branch merged to `main` via approved PR
- [ ] All AC scenarios have passing unit tests
- [ ] Unit test coverage meets threshold
- [ ] No TODOs, debug code, or commented-out blocks in merged code
- [ ] `sdlc-scrum-master` notified
```

A checklist does two things: it prevents the agent from stopping too early (missing items), and it makes the completion criteria unambiguous for you when you review the output. "Is this done?" becomes answerable in 30 seconds.

---

## The Curse of Instructions

One pattern I learned to avoid: the **monolithic spec**. One giant prompt that covers every possible scenario an agent might encounter. The temptation is to make it comprehensive — but there's a hard limit where adding more requirements actually _degrades_ performance.

The reason is context. When a prompt contains 50 rules, an agent's attention to each individual rule goes down. Research has shown this effect is real — it's called the ["curse of instructions"](https://maxpool.dev/research-papers/curse_of_instructions_report.html). Tested across GPT-4o, Claude 3.5, Gemini 1.5, and others: success rates drop from ~90% on a single instruction to as low as 15% when multiple constraints are combined.

The solution is separation of concerns. Instead of one agent with 50 rules, use 8 agents with 6-8 rules each. The developer agent doesn't need to know how to write a test strategy. The QA agent doesn't need the commit format rules. Each spec covers exactly what that agent needs — nothing more.

Concretely: when writing a SKILL.md, if a rule applies to this agent's outputs _and_ to another agent's inputs, it belongs in both. Don't try to centralize it in one place for consistency. Let each spec be complete for its role.

---

## The Checklist

Before handing any agent spec to an AI, run through this:

**Structure**
- [ ] Role summary: one paragraph, no ambiguity about what this agent owns
- [ ] Inputs: listed with source (which agent or human provides each)
- [ ] Outputs: listed as concrete artifacts with file paths or destinations
- [ ] Workflow: numbered steps, not bullet soup (a flat list with no order or dependencies)
- [ ] Definition of Done: checkboxes, not prose
- [ ] Rules section with ✅ always / ⚠️ ask / 🚫 never

**The Six Areas**
- [ ] Exact commands included (not "run the tests" — `uv run pytest -v`)
- [ ] Testing framework and coverage threshold specified
- [ ] File/directory structure explicit
- [ ] Code style shown by example
- [ ] Git workflow defined (branch format, commit format, PR target)
- [ ] Boundaries enumerated — what this agent must never touch

**Quality**
- [ ] No vague phrases ("best practices", "clean code", "make sure it works")
- [ ] Templates referenced for all output artifacts (not inline prose)
- [ ] Collaboration map: who this agent contacts for what
- [ ] Scope is tightly bounded — one role, not multiple

---

## Conclusion

At Level 4 SDLC — where humans write specs and AI implements and tests — the spec _is_ the product. Code is a side effect.

A vague spec produces a wrong-but-plausible result. A precise spec with checkboxes, hard stops, and real examples produces something you can trust to gate, ship, and audit.

Less art. More checklists in the end.

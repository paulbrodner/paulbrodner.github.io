---
layout: post
title: 'Two Loops: Fast for Side Projects, Gated for Everything Else'
date: 2026-08-18 09:00 +0000
categories: [Frameworks]
tags: [AI, SDLC]
comments: false
excerpt: "The design-build-ship loop was built for side projects I could throw away. For codebases other people depend on, I needed four approval gates instead of one — here's why that trade-off is on purpose."
---

In [my last post on the SDLC skills](/2026/from-building-to-orchestrating-sdlc-skills-that-changed-how-i-ship/), I described a fast loop — design, build, ship — that let me take two side projects from init commit to shipped in days. The velocity was real. But the post ended on a problem I didn't have a clean answer for yet: the loop optimizes story by story, and nothing in it protects the coherence of the whole product. Individual features work. The thing as a whole quietly drifts.

That problem gets worse, not better, the moment the codebase isn't yours alone to throw away.

A side project has one reviewer, no history to contradict, and a blast radius of exactly one person's afternoon if something goes sideways. A codebase your team depends on has none of that slack. A bad seam isn't a rough edge you notice later — it's someone else's incident. So I built a second loop for that context, and it looks nothing like the fast one.

---

## Two Different Problems

The fast loop assumes you can afford to find out you were wrong *after* code exists. Review happens once, at the PR. If the story was underspecified, you catch it in the diff, fix it, re-ship. That's a fine trade when the cost of being wrong is a wasted hour.

It's a bad trade when the codebase is shared, load-bearing, or already has years of decisions baked into it that a fresh agent session can't see. In that setting, the expensive mistakes don't happen in the code — they happen upstream, in the assumptions nobody wrote down before implementation started. By the time you're reviewing a PR, the ambiguity is already compiled in.

So the fix isn't a better PR review. It's moving the checkpoints earlier — before any code exists at all — and making each one something a human has to explicitly sign off on rather than glance past.

---

## The Four Gates

That's what `/bro-feature` is: a workflow with four sequential gates — **Product, Architecture, Program Design, Vertical Slices** — where each gate has to be explicitly approved before the next one starts, and none of them produce implementation code.

![bro-feature 4-gate workflow](/images/posts/bro-feature.jpeg)

The shape matters more than the label on any individual gate. Product comes first and stays free of implementation detail — it's forced to answer "what is this and why" before anyone's thinking about endpoints. Architecture comes next, and it has to read the existing codebase before proposing anything — never design against an imagined system. Program Design pins down types, signatures, and the call stack before a single test is written. Only then do Vertical Slices start landing code, one proven capability at a time. At every arrow in that diagram, you can revise or backtrack — the loop doesn't move forward on an assumption, it moves forward on an approval.

Compare that to the fast loop's one checkpoint per story, and the difference is the point.

---

## Why This Fixes What the Last Post Flagged

I named three specific failure modes in the last post. This workflow is a direct answer to each one.

**Ambiguity that compounds silently.** In the fast loop, a vague word like "toggle visibility" gets interpreted confidently and ships before anyone notices the gap. Gate 1 exists specifically to force that ambiguity into the open — no tech talk allowed until the problem and the success metric are stated plainly enough that there's nothing left to misread.

**An agent that doesn't push back.** Self-review catches obvious bugs, not "wait, doesn't this contradict what we built last week?" Gate 2 makes that check structural instead of hopeful — it reads the current codebase first, so a conflicting pattern gets caught before it's proposed, not after it's merged.

**Coherence that erodes across independently-shipped stories.** The fast loop has no mechanism for noticing that two features solved the same problem two different ways. The gated loop does, because Architecture and Program Design are evaluated against what already exists every single time, not just against the ticket in front of you.

---

## The Trade-off, Named Plainly

This is slower. Four approvals before a line of code exists is, by design, more friction than one approval after. That's not a flaw to optimize away — it's the actual mechanism. You're paying review time up front specifically so you don't pay debugging and re-architecture time later, in a codebase where "later" involves other people.

The choice between the two loops isn't about which one is better. It's about which mistake is cheaper where you're standing. On a side project you can rewrite in an afternoon, optimize for velocity and let the PR catch the rest. On a codebase that outlives the sprint, optimize for catching the wrong assumption before it has a chance to become code.

---

Three things I'd take away from this:

**The right loop depends on what breaks if you're wrong.** A fast loop and a gated loop aren't competing philosophies — they're tuned to different failure costs. Match the loop to the codebase, not to habit.

**Move the checkpoint to before the mistake, not after it.** Catching an ambiguous requirement in a PR is catching it too late — the assumption is already compiled into the implementation. Gates exist to catch it while it's still just a sentence.

**Coherence has to be checked against reality, not against the ticket.** A workflow that reads the existing codebase before proposing anything catches drift that a story-by-story review structurally cannot.

The fast loop taught me that velocity was never the constraint. The gated loop is what you build once you accept that, on a codebase that matters, correctness of the *assumption* is the constraint — and by the time it's code, it's too late to gate it.

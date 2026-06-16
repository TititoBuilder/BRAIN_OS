---
title: "Lesson 8 — The Session Loop and the Change Token"
course: gold_capstone
sequence: 8
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 3
---

Here's what you need to know about how your system remembers across sessions, and how it stays fresh without wasting effort — two pieces of machinery that solve the same underlying problem, which is that you and your tools both start each session with no memory.

Start with the loop. At the end of a working session, one tool gathers what happened — it reads your recent commits to see what you actually did, asks you what is still pending, and writes all of it into a dated archive. At the start of the next session, another tool reads that archive back, along with your project's contract and your open queue, and hands it all to you as one bundle of context. Close writes the archive. Start reads it. What you save at the end of today is exactly what loads at the beginning of tomorrow.

That loop is the whole answer to a hard problem. Neither you nor an assistant carries memory between sessions. Without this, every session would begin with twenty minutes of re-explaining what the system is and what you were doing. The archive is the baton passed from one session to the next, so work compounds instead of evaporating. And notice the honesty built in — the accomplishments come from reading your actual commits, not from asking you to remember. The machine records what it can prove you did. You fill in only what the commits cannot know.

Now the second piece — freshness, done cheaply. Your system keeps a local snapshot of what lives in your cloud storage. The question every session is whether that snapshot is still accurate, or whether something changed in the cloud since you last looked. The naive way to answer that is to re-scan the entire cloud storage every time. Slow, wasteful, many requests, most of them confirming nothing changed.

So your system does something smarter. The cloud service hands out a token — think of it as a bookmark marking the exact state of your storage at a moment in time. Your system stores that bookmark. Next session, instead of re-scanning everything, it asks the service one cheap question — has anything changed since this bookmark? If the answer is no, it skips the sync entirely and trusts the snapshot. Only if something actually changed does it do the expensive work of re-scanning. One cheap question replaces a full re-scan, almost every time.

That is a pattern worth keeping far beyond this system. When you need to know whether something changed, do not re-examine the whole thing by default. Ask the source if it changed, using whatever cheap signal it offers, and only do the expensive work when the answer is yes. Re-scanning everything to detect a change you usually will not find is effort spent confirming nothing.

And there is a quiet connection to the very first lesson here. The change token is itself a way of verifying against reality cheaply. Rather than assuming the snapshot is still good, or assuming it is stale, it asks the source directly and acts on the real answer. Even your freshness check is built on the same rule — do not assume, ask the thing itself.

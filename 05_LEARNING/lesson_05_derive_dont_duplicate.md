---
title: "Lesson 5 — Derive, Don't Duplicate"
course: gold_capstone
sequence: 5
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 3
---

Here's what you need to know about lists you maintain by hand versus lists the computer figures out for itself — because the difference between them is the difference between a system that drifts and a system that stays true.

You have seen both kinds in your own code, side by side, doing nearly the same job. One tool kept a hand-typed list of which topics to process. Every time you added a topic, you edited the list in the code. And because it was hand-maintained, it was fragile in two ways. It could list a file that no longer existed, so the tool would only discover the gap when it ran and failed. And it was long enough that the author had to add a guard against accidentally listing the same thing twice. A hand-maintained list needs a guard against its own mistakes. That tells you something.

The other tool did the opposite. Instead of a list, it scanned a folder and built the set of topics by reading each note's status. A topic registered itself the moment its status reached a certain level. There was no list to maintain, because the list was derived from reality every time it ran. Add a topic, set its status, and it appears — automatically. Remove a topic, and it disappears. The tool cannot list a file that does not exist, because it only ever looks at files that do.

That is the core idea. When you derive a list from the actual state of things, the list cannot drift, because it is rebuilt from truth on every run. When you duplicate that information into a hand-maintained list, you have created a second copy that must be kept in agreement with the first — and it will not stay in agreement, because keeping two things in sync by hand is a tax you pay forever and eventually forget to pay.

Now, here is the honest nuance, because the rule is not absolute. Sometimes deliberate duplication is the right call. You saw a tool that copied a few helper functions from another tool on purpose, with a comment explaining exactly why — to stay independent and runnable on its own. That is fine. The difference is that it was deliberate and documented. The danger is the duplication that just happens — two copies of the same file in two folders, the good pattern written in one place and never carried to the other, a function copied and then quietly renamed so the two versions start to diverge. Undocumented duplication always rots, because nothing reminds you the copies exist.

So the working rule is this. Derive what changes often. Pin by hand only the few stable things that almost never move, and when you do duplicate on purpose, write down why. The moment you find yourself maintaining the same information in two places, ask whether one of them could simply be computed from the other. Usually it can. And when it can, you have removed an entire category of future bug — the slow, silent drift between two things that were supposed to match and stopped.

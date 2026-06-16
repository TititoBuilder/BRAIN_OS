---
title: "Lesson 3 — The id: Crisis"
course: gold_capstone
sequence: 3
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 4
---

Here's what you need to know about the day your app played the wrong audio — because it's the best story you have for why you check things instead of trusting them.

The symptom was small and maddening. You'd tap a topic in your study app, and sometimes the audio that played wasn't the lesson you asked for. Not every time. Just often enough to make you doubt the whole thing. The easy reaction would have been to assume the app was flaky and move on. You didn't. You went looking for the actual cause.

Start with how your app finds audio. When you tap a topic, the app looks that topic up in an index — a simple list that maps each topic to its audio file. There are two ways an entry in that list can point at a file. It can point by file identity — a unique Drive ID that means one exact file, no ambiguity. Or it can point by path — basically a filename. And here's the trap: when the app gets a filename instead of an ID, it can't fetch the file directly. It has to search Drive by that name, and take whatever comes back first. If two files happen to share a name, the search can hand back the wrong one. That's your wrong audio. Not flakiness — a name collision resolved by a guess.

So the next question is: why were any entries stored as names instead of IDs? You traced it back to the script that publishes audio. When it uploaded a file to Drive, Drive handed back the file's unique ID — the exact thing you needed. And the script threw it away. It captured the upload, ignored the returned ID, and wrote the filename into the index instead. The fix was two lines: catch the ID the upload already gives you, and write it in the reliable identity format. The information was never missing. It was being discarded at the moment it mattered most.

Here's the part worth sitting with. Three separate things you'd noticed over weeks — the occasional wrong audio, a vague note to "convert old entries someday," and a memory that filename search was unreliable — were not three problems. They were one problem, wearing three masks. You only saw that they were the same thing because you followed the thread all the way down instead of patching the surface.

And notice what found it: not cleverness, not a guess about what was probably wrong. You read the actual code, line by line, and watched a returned value get dropped. The bug was invisible from the outside and obvious from the inside. That's the whole lesson, and it's the same rule that runs through everything you've built. The thing that looks settled — "the app is just flaky," "the index is fine" — is a claim. And a claim isn't true until you've checked it against what the code actually does. You checked. You found the discarded ID. You fixed the source, not the symptom. Remember that the next time something is wrong "sometimes."

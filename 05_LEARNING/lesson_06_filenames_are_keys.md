---
title: "Lesson 6 — Filenames Are Machine Keys"
course: gold_capstone
sequence: 6
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 3
---

Here's what you need to know about your filenames — because in your system, a filename is not a label for humans. It is a key that machines use to find things, and that changes the rules for how you name.

Think about how a single topic flows through your system. There is the source note, the audio file, the transcript, the index entry, and the lookup the app does to play it. Every one of those references the same identifier — the machine key for that topic. The key is what lets five separate systems agree on what they are talking about without having to re-match anything. The key is the join. It is the thread that holds the whole pipeline together.

That gives filenames a job most people never assign them. The name is not decoration. The structure of the name carries meaning the code reads. In your audio library, the suffix on a file tells the system what kind of audio it is — a raw voiced chapter, an anchor, a combined version. The code looks at the name and decides how to handle the file based on what the name says. The name is data.

This is powerful, and it is exactly why it is fragile. Because the code trusts the name to follow a convention, the moment a name breaks the convention, the code mis-handles it or fails to see it at all. You have a function that classifies chapters as core or alternate by counting the segments in the filename. Add one extra word to a core chapter's name and the code now thinks it is an alternate. The file did not change. Only its name did, and the meaning flipped, silently.

And here is where the discipline shows its cost when it slips. Your session files drifted into four different naming conventions over time. Four. So the tool that reads them has to carry four separate patterns just to recognize the same kind of file. That is the tax of undisciplined naming — when the key format is not held steady, the code that reads the key multiplies to keep up. One clean convention needs one pattern. Four sloppy conventions need four, forever, until someone cleans them up.

The good news is the system was built to catch this. When the cataloging tool meets a file whose name it does not recognize, it does not silently skip it. It prints a warning naming the file. That is how naming drift gets caught early — a new, off-convention name shows up as an unrecognized line, and that line is your signal to either rename the file or accept a new pattern. There is even a tool that renames non-standard files back to the canonical form, with a preview mode so you can see the plan before anything moves.

So treat names as keys, not captions. Pick a convention and hold it, because the code depends on it. When you see an unrecognized-name warning, do not ignore it — it is the early signal of drift. And remember the deeper point. The reason your four layers stay in sync is that they all agree on the same key. Break the key and they stop agreeing. The filename is not for you. It is for the machine, and the machine is strict.

---
title: "Toolchain Architecture"
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 4
---

Here's what you need to know about how every tool you run is actually wired — because once you see the pattern, every shortcut in your terminal stops being magic and becomes readable mechanics.

Every tool you type at the terminal follows three layers. There is the shortcut, the brain, and the output. These three layers never overlap, and that separation is what makes the system debuggable.

The shortcut is a function in your PowerShell profile. It is one word — session-start, git-session, cc. When you type it and press enter, the profile function runs. And here is the important thing: the profile function does almost nothing. It calls something else. That is its entire job. The profile is the door, not the room.

The brain is a Python script in your 09_TOOLS folder. Python does the actual work — reading files, filtering data, building output, deciding what to write and where to write it. Python is used here because it handles encoding correctly, it can express real logic without fighting the language, and it produces consistent results on Windows. PowerShell can call things and move files, but Python is where the reasoning lives.

The output is whatever the script produces. It might be a context string copied to your clipboard. It might be a file written to disk. It might be an upload to Drive or a message sent to Telegram. The output is specific to the task, but the pattern is always the same — shortcut calls brain, brain produces output.

Walk through a real example. You type git-session. The profile function runs and calls the task session script with an argument telling it the task is git. The script opens Queue dot md, finds every open item in the In Progress section, then finds your git note files and reads the first five lines of each — just the headers, not the full content. It assembles those pieces into one focused string, sends it to the Windows clipboard, and exits. The profile then prints a confirmation line. From your perspective it was one word. From the system's perspective it was a three-layer chain.

Walk through another. You type session-start. The profile calls the graph maintainer script first, which updates your project context files. Then it calls the session start script, which reads health data, checks the queue, and copies the full context to your clipboard. Two scripts, one shortcut, one coherent result.

Walk through the simplest one. You type cc. The profile calls Claude Code with a flag that bypasses permission prompts. That is the entire chain. One word in, one longer command out. The profile exists so you never have to remember the flag.

The principle that holds this together: the profile is always the door, the Python script is always the room. The profile knows where the room is. The script knows what to do inside it.

When something breaks, you know exactly which layer to look at. The shortcut runs but the wrong output comes out — the Python script has a bug. The shortcut does not run at all — the profile has a bug. The output is right but the data inside it is stale — the files the script reads have a problem. Three layers, three completely separate failure modes. You never have to guess which one to investigate.

Your entire 09_TOOLS folder is the brain layer. Every script in it is called by something — a profile function, another script, or Claude Code directly. Reading 09_TOOLS_INDEX dot md tells you what every brain does and what calls it. That index is the map to the room.

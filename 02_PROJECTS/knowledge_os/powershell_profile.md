---
title: "PowerShell Profile"
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 3
---

Here's what you need to know about the file that runs before you type a single command — because most of what feels like magic in your terminal is actually just this one script doing its job.

Every time you open a PowerShell terminal, Windows looks for a profile file and runs it automatically. You do not trigger it, you do not import it, you do not think about it. It runs. By the time the cursor appears and waits for your first command, that script has already finished. Everything it defined is live and ready.

What does it define? Functions, mostly. Your profile contains shortcuts that wrap longer commands you would otherwise have to type in full every time. When you type "cc" and a Claude Code session opens, that works because your profile created a function called "cc" that runs the full Claude startup sequence. When you type "session-start" and the vault loads, same thing. These are not built-in commands. They exist because your profile put them there. Remove the profile and those names mean nothing. The terminal does not know them.

The profile also does something less visible but equally important: it loads your secrets. Near the top of your profile, there is code that reads the .env file at the BRAIN_OS secrets path and sets each key as a live environment variable. This happens before you do anything. So when a Python script later asks the system for the Telegram token or the Anthropic key, the value is already there — not because the script found the file, but because the profile already loaded it into the running session. That is the relay. Profile reads the file once; everything that runs after inherits the result.

Your profile file lives at a path inside OneDrive, which means it syncs across machines. Change a function on one machine and the updated version follows you to the next login. This is intentional. The profile is configuration that travels with you, not with the machine.

Editing the profile is just editing a text file. Open it in VS Code, make your change, save. But the current terminal session is already running with the old version in memory. To apply the change without closing and reopening the terminal, run one command: dot, space, then the PROFILE variable. This re-executes the profile in the current session, replacing the old definitions with the new ones. You do not need to restart. The terminal picks up the change immediately.

Think of the profile as the thing that turns a generic PowerShell window into your working environment. Without it, you have a blank shell that knows nothing about your system. With it, you have a configured workspace that already knows your shortcuts, your secrets, and your tools — before you say a word.

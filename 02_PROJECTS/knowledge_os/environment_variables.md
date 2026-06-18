---
title: "Environment Variables"
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 3
---

Here's what you need to know about how secrets travel through your system — because if you have ever wondered why a Python script can find your API key without you typing it in, this is the answer.

An environment variable is a named value that the operating system makes available to every process running on the machine. Think of it as a bulletin board the entire system can read. Any script, any tool, any program that starts up can look at this board and see what is posted there. The name is the label; the value is the content. Your Anthropic key, your Telegram token, your Google credentials — each one is a named entry on that board.

In PowerShell, you read them through a special path prefix. But you rarely need to type that directly. The more important question is how the values got there.

Your system uses a .env file as the single source of truth for secrets. It lives in your BRAIN_OS folder under the APIs path. This is a plain text file — key-equals-value pairs, one per line. It is not a script. It does not run. It is data.

What makes it useful is the profile. Every time a terminal opens, your PowerShell profile reads that .env file and loads each entry into the session as a live environment variable. So by the time you start typing commands, all your secrets are already available to everything that runs in that session. You did not do anything. The profile did.

Python scripts on the other side pick those values up in one of two ways. If the variable is already in the environment because the profile loaded it, the script reads it directly through the standard environment API. If the script runs in a context where the profile did not load — a subprocess, a cron, a test runner — the script calls load_dotenv itself, which reads the same file and sets the same values. Either path leads to the same result: the script gets the value it needs without it being typed or hardcoded anywhere.

That last part is the discipline. Secrets must never appear in source code. Not in scripts, not in config files, not in comments. Those files get committed to git, and git is not private by default. A secret committed to a repository is a secret that needs to be rotated immediately. The entire point of the .env file and the environment variable pattern is to keep the value out of the code entirely.

The payoff is maintenance. When a token expires and you generate a new one, you update one line in one file. Everything that reads that key — every script, every tool, every session — picks up the new value automatically. One place. One edit. No hunting through scripts to find every hardcoded copy.

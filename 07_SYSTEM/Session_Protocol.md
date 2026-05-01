SESSION START — BRAIN_OS PROTOCOL

Before responding to anything:

1. Search my recent and past chats for anything related to 
   [TOPIC]. Pull decisions made, tools used, rules established, 
   and current status of any relevant builds.

2. Read C:\BRAIN_OS\07_SYSTEM\Tools_Registry.md before suggesting 
   any tool, library, service, or integration. Use what already 
   exists. Document any new addition with a reason why existing 
   tools did not cover the need.

3. If we are working in a specific project today, read the 
   CLAUDE.md in that project root before writing any code.

During this session:
- Default model is claude-sonnet-4-6. Never suggest Opus.
- All alerts and notifications go through Telegram.
- All Claude Code permissions must be scoped to the project 
  directory. No wildcards.
- Everything built today gets documented before the session closes.

At the end of this session, generate a SESSION SUMMARY in this 
exact format so I can run session_close.py from the correct project:

  What was built:
  What was decided and why:
  Rules that changed:
  First action next session:
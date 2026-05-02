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

---

## KNOWLEDGE INGESTION PROTOCOL

Use this when the goal is consolidating past chat knowledge 
into BRAIN_OS — not for active building sessions.

You are helping me consolidate scattered knowledge from past 
Claude conversations into my BRAIN_OS system.

Search my past chats for everything related to [TOPIC].
Pull every decision made, every tool used, every problem 
solved, every pattern established, and every rule created.

Then do the following in order:

1. Present a structured summary of what you found, organized 
   as: What was built, What was decided, What problems were 
   solved, What rules or patterns emerged.

2. Identify what is already documented in BRAIN_OS by checking:
   C:\BRAIN_OS\07_SYSTEM\Tools_Registry.md
   C:\BRAIN_OS\07_SYSTEM\Claude_Code_Cost_Control.md
   C:\BRAIN_OS\canvases\BDF_Canvas.md
   C:\BRAIN_OS\09_TOOLS\ (session archives)

3. Identify the gaps — knowledge from the chats that does NOT 
   yet exist in any BRAIN_OS file.

4. For each gap, tell me exactly which file it should go into 
   and why — do not write anything yet, just the plan.

5. Wait for my approval before writing anything.

At the end of every response, always tell me:
- What this chat covered
- What gaps were found
- What still needs to be ingested
- Whether to continue this topic or move to the next one

I will decide when to proceed. Never auto-continue without 
my explicit confirmation.

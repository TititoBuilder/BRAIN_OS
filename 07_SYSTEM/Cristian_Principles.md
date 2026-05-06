---
tags: [personal, learning, principles, mental-models]
updated: 2026-05-04
---

# Cristian's Principles

Personal mental models and frameworks proven through completing real work.
This is not a reference manual — it's a collection of hard-won insights
that have been internalized through hands-on experience and successful
task execution.

**Rule for adding entries:** Only add knowledge here after completing a task
that proves you've fully learned and can apply the principle. Theoretical
understanding doesn't count. Demonstrated competence does.

---

## MCP Tool Selection Framework

**Learned from:** Completing Telegram integration across BDF and CristianConstruction
projects (commits 7c765fc and 9ce37d4, May 2026)

**The Core Principle:** Use the most direct tool that accomplishes the task
correctly. Only reach for abstraction layers when they add value beyond
what the direct tool provides.

Think of tool selection like choosing transportation. Walking is direct with
full control over your path. Driving adds machinery between you and the
destination. Sometimes that machinery is worth it because you need to go
ten miles. Sometimes it's overkill because you're going fifty feet.

**Three Questions for Deciding When to Use an MCP:**

Ask these in order. Stop at the first yes.

**Question One: Does this task require capabilities that only the MCP provides?**

If the MCP can do something the direct tool fundamentally cannot do, use the MCP.
For example, creating GitHub pull requests with reviewers and labels is a GitHub
feature, not a git feature. The GitHub MCP can do this, bash git commands cannot.
Context7 can fetch current library documentation at specific versions from source
repositories. Bash cannot. The Obsidian MCP understands vault structure and can
maintain link integrity. Text file editing cannot.

If the answer is yes, use the MCP. If no, proceed to question two.

**Question Two: Does the MCP provide a significantly simpler interface for a complex operation?**

If the MCP turns a fifteen-step manual process into a two-step automated process,
that abstraction is adding value. For example, querying all open issues across
multiple repositories, filtering by label, and extracting statistics would require
dozens of manual API calls you'd have to orchestrate yourself. The GitHub MCP might
provide a single high-level query that handles all of that. Similarly, searching
and updating multiple interconnected Obsidian notes while maintaining link integrity
is much simpler through the Obsidian MCP than editing files one by one.

If the answer is yes, consider the MCP. If no, proceed to question three.

**Question Three: Do I need to learn how the MCP works for future use cases?**

Sometimes you choose a tool not because it's optimal for the current task, but
because you're building familiarity with it for future tasks where it will be
necessary. This is valid as long as you understand you're in learning mode rather
than optimization mode. You're accepting temporary inefficiency to build long-term
capability.

If the answer is yes, use the MCP as a learning exercise. If no, use the direct tool.

**Practical Example — Feature Development Workflow:**

When adding a new feature to a FastAPI project and documenting it, the natural
tool sequence looks like this. You do local development and testing using bash
commands and Claude Code's file editing tools because those are direct and
transparent. When you need to understand how a library works, you use the Context7
MCP because it fetches authoritative current documentation that bash cannot access.
When committing your changes, you use bash git commands because commit and push
are straightforward git operations that need no abstraction. When creating a pull
request with reviewers, labels, and issue links, you use the GitHub MCP because
those are GitHub-specific features that don't exist in git. When the pull request
is approved and you're ready to merge, you use bash git commands again because
merging is a core git operation. When updating your BRAIN_OS documentation to
reflect the new feature, you use the Obsidian MCP because it understands vault
structure and can maintain knowledge graph connections.

Each tool gets used exactly where it provides unique value. The MCPs are not
replacing core tools like bash, git, and text editors. They're augmenting them
for specific scenarios where integration and automation add real value that the
direct tools cannot match.

**What This Principle Prevents:**

Using MCPs everywhere indiscriminately just because you want practice creates
slowness and obscures what's actually happening. Using a drill to cut boards
just because you're trying to learn the drill makes you inefficient and produces
poor results. The right tool for the right job is what makes you effective.
Building MCP fluency means recognizing the specific scenarios where each MCP
provides unique value, not forcing their use in situations where simpler direct
tools work better.

---

## Name Verification Pattern

**Learned from:** Obsidian MCP hanging 7+ minutes due to wrong package name (2026-05-03)

**The Core Principle:** Never assume abbreviations map to the right tool. Always verify the full package name before configuration.

**The Incident:** "obs" was registered in MCP config assuming it meant Obsidian. "obs" is OBS Studio (streaming software). "obsidian" is Obsidian (note-taking). Two completely different tools with a 3-letter vs 8-letter difference. The MCP showed "Connected" but hung on every tool call.

**Rule:** Before registering any tool, service, or package:
1. Look up the full, exact package name (npm, pip, etc.)
2. Verify what the abbreviation actually expands to
3. Never assume — always confirm with the simplest test call

**When this saves you time:**
- MCP configuration (package names often differ from tool display names)
- pip/npm installs (wrong package = wasted time or security risk)
- Service endpoints (similar names, different services)

---

## Knowledge Management Principles

**Learned from:** Building the BRAIN_OS knowledge ingestion pipeline (2026-05-03)

Five principles proven through constructing a working automation system:

**1. Chat data is the most valuable asset**
Every session produces decisions, fixes, patterns, and breakthroughs. Unstructured, this data is lost within days. Structured via SESSION_COMPILE_TEMPLATE, it becomes portable, searchable, and book-ready.

**2. Structure enables extraction**
Templates make knowledge portable. The same information in an unstructured chat vs a session compile is the difference between lost context and a book chapter. The template is the extraction mechanism.

**3. Links create intelligence**
Wiki-links turn isolated notes into a knowledge graph. `[[Custom_Agent_TTS]]` → `[[Audio_Systems_Comparison]]` → `[[Data_Science]]` — each link multiplies the value of every node it touches.

**4. Automation removes friction**
Zero manual copy/paste means zero lost knowledge. Each manual step is a failure point. A pipeline that runs without asking for help is the only kind that actually runs consistently.

**5. Visibility drives progress**
Seeing what you've built (domain dashboards, graph view) motivates continued building. Invisible progress feels like no progress. The 01_DOMAINS/ dashboards exist for this reason.

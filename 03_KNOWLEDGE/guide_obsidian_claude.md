# Guide: Obsidian and Claude — Building a Second Brain

Obsidian is a note-taking application that stores everything as plain markdown files on your hard drive. No cloud sync required. No subscription. No proprietary format. Every note you write is a text file you own completely.

The reason Obsidian matters in a developer workflow is not the note-taking itself. It is the knowledge graph. Every note can link to every other note using double-bracket syntax. Over time those links build a map of how your ideas connect. A note about venv isolation links to the MCP trust model which links to the BRAIN_OS build process which links back to the architecture principles. The graph makes relationships visible that would otherwise stay buried in separate documents.

My vault lives at C drive backslash BRAIN_OS. It is organized into numbered folders. Zero zero is the dashboard with the main canvas overview. Zero one is domains — the high-level categories of knowledge like AI Engineering, Creative Systems, and Data Science. Zero two is agents — documentation for each AI agent I have built. Zero two is also projects — one node per active project with status, paths, and dependencies. Zero seven is system — the proven principles and navigation shortcuts. Zero nine is tools — scripts like graphify and session close.

The Obsidian MCP connects Claude Code to the vault. When it is working correctly, Claude Code can read any note, create new notes, search for content, and follow wiki links through the graph. This turns the vault from a personal reference into an active working memory that Claude can query during a session.

The MCP has one critical rule. Always verify it works with an actual tool call before trusting the Connected status. The Obsidian MCP spent an entire session showing Connected while hanging indefinitely on every tool call. Connected means the process started. It does not mean tools work. The fix was a configuration update that changed how the vault name was passed to the server. After the fix, tool calls respond in about 15 seconds.

The workflow that connects sessions to the vault has five stages. First you work on something real and document what you learned in the conversation. Second you run session close dot py which extracts the key facts and decisions into a structured markdown file. Third that file gets committed to BRAIN_OS with a descriptive message. Fourth the Obsidian graph automatically picks up the new links and updates the canvas. Fifth the next session starts by running graph maintainer to load the project context before any work begins.

The most important document in the vault is Cristian Principles dot md. It lives in the zero seven system folder. Every entry in that file was earned through completing real work, not from reading about patterns. The rule is strict: no entry gets added until the knowledge is proven through a finished task. This keeps the document from becoming a collection of things you read once and thought sounded smart. Every line in that file is something that actually happened in your system.

The second most important document is Navigation Shortcuts dot md. It is the single source of truth for every path, alias, and project location across your entire ecosystem. When a path changes anywhere, you update it there first. Every other document points to it rather than storing its own copy of the path.

The combination of Obsidian and Claude creates a feedback loop. Claude helps you build things. The things you build generate knowledge. The knowledge gets captured in Obsidian. Obsidian feeds context back to Claude for the next session. Each session makes the next one more precise. The vault is not a archive. It is a growing intelligence layer for everything you build.

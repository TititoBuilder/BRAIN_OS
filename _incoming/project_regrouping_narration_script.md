Welcome to your project regrouping guide. This audio is different from the others. Instead of teaching you a new tool, this one maps out everything you've built so far, where each project stands, what's pending, and how all the pieces connect. Think of this as your personal state of the union. After listening, you'll have a clear mental model of your entire development landscape.

Chapter one. Your machine and environment.

You're running a Predator Helios Neo laptop with Windows 11. Your username on the machine is titit, so your home directory is C colon backslash Users backslash titit. You have an NVIDIA RTX 5070 Ti graphics card with CUDA 13.2 driver support, which means you can run GPU-accelerated workloads like AI model inference and video processing significantly faster than on CPU alone.

Your system Python is version 3.12.10, installed at C colon backslash Users backslash titit backslash AppData backslash Local backslash Programs backslash Python backslash Python312. This is your global Python. You never install project packages into this one. Every project gets its own isolated virtual environment.

Your development tools include VS Code as your primary editor, PowerShell as your terminal, and Git for version control. A critical PowerShell lesson you've learned: always use where dot exe python, never just where python. In PowerShell, where is aliased to Where-Object and silently returns nothing. The dot exe version bypasses the alias and gives you the real path.

Another critical lesson: never put Python projects inside OneDrive. OneDrive's file sync locks files during upload, which causes random failures during pip install and venv operations. All your projects now live outside OneDrive, and you use Git and GitHub for version control instead.

Chapter two. Your project landscape.

You have four active projects on your machine. Let's go through each one.

Project one. BreakingDown Futbol, also called BDF or the soccer content generator. This lives at C colon backslash Dev backslash Projects backslash soccer-content-generator. It has its own virtual environment inside that folder. This is your main platform project. It's a multi-agent system built with Python and FastAPI that generates soccer content for Twitter and X. The architecture includes a content agent that writes posts, an image agent that generates visuals using Together AI's FLUX model for daily posts and OpenAI's DALL-E 3 for premium content, and a Twitter agent that handles posting through the Twitter API v2 via tweepy. The system uses RAG, which stands for Retrieval Augmented Generation, with a vector store to pull relevant soccer knowledge before generating content. This project is the most mature of your four projects and represents your core platform vision.

Project two. CristianConstruction, your custom agent project. This lives at C colon backslash Dev backslash CristianConstruction. It also has its own isolated venv. This project is a custom AI agent you've been building. The details of its current state aren't as well documented in recent conversations, but it follows the same architecture patterns as your BDF project.

Project three. The Read-Along App. This lives at C colon backslash Users backslash titit backslash Projects backslash read-along-app, with backend and frontend subdirectories. It's a web application for uploading MP3 files, transcribing audio with word-level timestamps using OpenAI's Whisper model, and synchronizing word highlighting during playback. The stack is Python with FastAPI and Whisper for the backend, and React with Vite for the frontend.

Current status of the Read-Along App: the clean project structure is established outside OneDrive. PyTorch 2.11.0 with CUDA 12.8 support has been installed in the backend venv, matching the pattern used in your other two project venvs. What's remaining before any app code can be written: CUDA verification by running torch dot cuda dot is available, FFmpeg system installation, and Whisper installation.

Project four. The Resolve MCP Server. This is your newest project, built today. It lives at C colon backslash Users backslash titit backslash Projects backslash resolve-mcp-server. This project connects Claude Desktop to DaVinci Resolve 20 through an MCP server. Since Resolve 20 broke its external Python scripting API, you built a workaround using pyautogui for keyboard automation and pywinauto for window focus management. The MCP server exposes Resolve's editing commands as tools that Claude can call through natural language. You can say things like "play the timeline" or "cut at the playhead" in Claude Desktop's chat tab, and the server sends the corresponding keyboard shortcut to Resolve.

Key discovery from this project: Resolve 20's scripting port 20321 is internal IPC only and cannot be used for external automation. The fusionscript DLL loads fine but the protocol handshake fails. Pyautogui was the successful workaround. Also important: in Claude Desktop, the chat tab is the speech bubble icon, not the Code tab.

Chapter three. Your knowledge system.

You've built a personal knowledge base at C colon backslash Knowledge. This folder is organized by domain. Inside it you have BDF for BreakingDown Futbol reference material, Dev for development and programming knowledge, Hardware for machine and GPU documentation, Personal for personal reference files, and Claudeguide for the Claude learning materials we've been building together.

Your learning workflow follows a specific pattern that's now saved in Claude's memory. When you need to learn a new subject, you generate extended audio guides using Microsoft's Edge TTS with the en-US-GuyNeural voice. You get both the narration script as a text file and a Python generator script. You save everything to Knowledge under a topic-specific folder. You listen to the audio first to build foundational knowledge, then read the text scripts chapter by chapter for detailed reference. Finally, you back up everything to Google Drive by dragging and dropping from File Explorer to drive dot google dot com in your browser.

This system is now baked into Claude's memory across all conversations. In any new chat, you can say "create a learning guide for" followed by any topic, and then say "using my audio learning system" and Claude will know exactly what to produce.

Chapter four. Your workflow discipline.

You follow strict rules across all projects, and these rules exist because you learned the hard way what happens when you skip them.

Rule one. One command at a time, with confirmed output before proceeding. Never chain dependent commands.

Rule two. Always verify the active virtual environment with where dot exe python before any pip install. This prevents accidentally installing packages into the wrong project or into your global Python.

Rule three. Never share virtual environments between projects and never activate one venv on top of another. Every session starts with a fresh terminal and explicit venv activation.

Rule four. Estimate costs before any paid API call. Whether it's Together AI, OpenAI, or any other service, you check the per-call cost before running anything that charges money.

Rule five. All commands must be translated to Windows PowerShell. You don't use Unix or macOS shell commands. When Claude gives you a command, it needs to work in your environment.

Chapter five. Tools and infrastructure across projects.

All three Python projects share the same PyTorch installation pattern. They all use CUDA 12.8 wheels installed with the dash dash index-url flag pointing to https colon slash slash download dot pytorch dot org slash whl slash cu128. This consistency is intentional. The same PyTorch version, the same CUDA runtime, the same mental model applies everywhere.

For text-to-speech, you use the edge-tts Python package with the en-US-GuyNeural voice. This is Microsoft's neural TTS engine and produces natural, human-sounding audio. It's used for your learning guides and could be integrated into any project that needs audio narration.

For audio processing in general, you've worked with UVR, which is Ultimate Vocal Remover, for isolating vocals from music. You've used 4K Video Downloader for extracting audio from YouTube. And you've set up OBS for screen recording with your Elgato capture card, using NVIDIA NVENC encoding on your RTX GPU.

For video editing, you use DaVinci Resolve 20, which you've now connected to Claude through the MCP server using pyautogui automation.

Chapter six. What's pending across all projects.

Let's get specific about what's unfinished so you know exactly where to pick up.

BDF Soccer Content Generator. This project is the most complete. The main pending items from recent conversations were integrating real AI-generated images through Together AI's FLUX model and DALL-E 3, replacing the earlier stock photo approach. The image agent needs retry logic for rate limit errors, specifically handling 429 responses with exponential backoff. There was also discussion about adding a TTS narration feature to generate MP3 audio for each post, using the tts agent module we designed.

Read-Along App. Three infrastructure steps remain before any application code. First, run torch dot cuda dot is available in the backend venv to verify GPU access. Second, install FFmpeg at the system level, either through Chocolatey or by downloading from the official site and adding it to PATH. Third, install OpenAI Whisper with pip install openai-whisper. Once those three are done, you can start building the FastAPI endpoints and React frontend.

Resolve MCP Server. The basic server is working. The next steps documented in the session are: adding more tools like color page shortcuts and marker colors, building a BDF highlight reel automation script using the ResolveController class, adding a jump-to-timecode tool, adding a playback speed control tool, and potentially installing Resolve 18.6.6 alongside Resolve 20 for full Python API access since the older version's scripting actually works.

Chapter seven. Your file structure overview.

Here's your complete directory layout as it stands.

C colon backslash Dev backslash Projects backslash soccer-content-generator. Your BDF bot with its own venv.

C colon backslash Dev backslash CristianConstruction. Your custom agent with its own venv.

C colon backslash Users backslash titit backslash Projects backslash read-along-app. Your read-along app with backend and frontend subdirectories, backend has its own venv.

C colon backslash Users backslash titit backslash Projects backslash resolve-mcp-server. Your DaVinci Resolve MCP server with its own venv.

C colon backslash Knowledge. Your personal knowledge base, organized into BDF, Claudeguide, Dev, Hardware, and Personal subfolders.

Other notable folders on your machine include: audio underscore output, which may be referenced by running scripts. Session underscore Resumes, which stores session context files for your bot. BDF underscore Book with 16 chapters of your book project. And the chapters folder containing chapter files numbered 1 through 16.

Chapter eight. How everything connects.

Here's the big picture view of how your projects relate to each other.

BDF is your content platform. It generates soccer content with AI and posts it to Twitter. The Read-Along App is a separate tool that could eventually complement BDF by creating interactive read-along experiences from soccer commentary or post narrations. The Resolve MCP Server is your video editing bridge, which could be used to automate highlight reel creation for BDF content. And the CristianConstruction agent is your custom AI agent project that could eventually orchestrate workflows across all the other projects.

The Claude learning system you've built, the Claudeguide folder with MP3s and text scripts, is your personal education infrastructure that supports everything else. As you learn new tools like Claude Code, DaVinci Resolve, Docker, or Git branching, you generate audio guides, absorb the knowledge, and apply it across all your projects.

Chapter nine. Recommended next actions in priority order.

Based on everything that's pending, here's a suggested priority order for what to tackle next.

Priority one. Finish the Read-Along App infrastructure. It's three commands away from being ready for application code. CUDA verification, FFmpeg install, Whisper install. Completing this removes a hanging incomplete project from your mental load.

Priority two. Expand the Resolve MCP Server. You proved the concept works today. Adding more tools while the architecture is fresh in your mind will be faster now than later. Focus on the editing commands you actually use most in your BDF highlight workflow.

Priority three. BDF image agent improvements. The retry logic and DALL-E 3 integration are well-defined tasks that can be tackled in focused sessions.

Priority four. Explore Claude Code for your BDF project. Now that you understand what Claude Code is from the audio guides, try it on your most mature project. Create a CLAUDE.md file for the soccer content generator and let Claude Code help you with the pending improvements.

That wraps up your project regrouping guide. You now have a complete mental map of every project, every pending task, every file location, and how it all connects. Use this as your compass. When you sit down to code, you know exactly where to pick up.

Back up this file to Knowledge backslash Claudeguide and to Google Drive. Then pick your priority and let's build.

This has been your project regrouping guide. Stay locked in.

---
title: "Dev Workflow"
knowledge_os_status: Learning
voice: af_heart
estimated_minutes: 3
---

Here's what you need to know about the loop between writing code and seeing it work — because understanding the difference between local iteration and production deployment is what separates fast building from slow, anxious building.

VS Code is the editor. It is where you write code. It has no server, it makes no requests, it deploys nothing. It is a text editor with awareness of your project structure. When you save a file in VS Code, the file changes on disk. That is all.

The development server is a separate thing entirely. You start it by running a command that launches a local process. That process watches your source files and the moment you save a change, it rebuilds the affected piece and pushes the update to your browser automatically. The browser refreshes in under a second. This is Hot Module Reload — the mechanism that makes iteration feel instant. You change a component, save it, look at the browser, and the new version is already there.

This loop — change a file, see the result immediately — is your primary building tool. It is how you learn whether something works before committing to a deploy. The dev server runs locally on your machine, serving your app at a local address. But here is what matters: it still calls your Railway backend for real data. When you test a feature that loads audio, it fetches from the same production backend the live app uses. So you are iterating in isolation on the front end while still working with real audio, real transcripts, real indexes.

When a feature is done — actually done, not done for now — you stop the dev server and build. The build command compiles your source files into an optimized bundle that browsers can load efficiently. This produces static files. Those files are what Vercel serves to your users.

Deployment pushes those files to Vercel. A preview deploy gives you a staging URL — a live, shareable version of the app that is not your production URL. This is useful for reviewing a change before committing it publicly. A production deploy replaces what users see when they visit your real app URL.

The discipline is this: never deploy while you are still iterating. The dev server is for figuring things out. The build is for confirming something works. The deploy is for publishing something finished. Mixing those stages means users see in-progress work, and you spend time managing a deployed state instead of building.

One more thing to hold: when you close the terminal, the dev server dies. It is a local process tied to that terminal session. It is not a service, it is not deployed, it is not running on any server. The moment that window closes, it is gone. Your production app keeps running because it lives on Vercel. Your local dev session runs only while your terminal is open.

# Read-Along App — Build Session
## How a Knowledge OS Gets Built, Debugged, and Shipped

This chapter documents the full development session of May 30, 2026 — covering diagnostic
thinking, pipeline gaps, new features shipped, and the engineering principles earned through
real work. Every principle here was proven through execution, not theory.

---

## The Problem That Started Everything

The session opened with a simple complaint: the karaoke feature was missing from the Listen tab.
Words were not highlighting as audio played. The audio worked. The dropdown worked. But the
synchronized word highlighting — the entire point of the read-along experience — was gone.

The wrong instinct would have been to rewrite the component. The right instinct was to investigate
before touching a single line of code.

---

## Never Debug Assumptions. Debug Reality.

This is the most important principle earned in this session. Before writing any fix, you must
verify each layer of the system independently. The bug lives at the layer where reality diverges
from your assumption.

There are three layers to check, always in this order.

The first is the code layer. What does the source actually say? Using git show and git diff,
we confirmed the karaoke code existed and was correct. The component fetched transcripts,
tracked the active word index, and rendered highlighted spans. The code was not the problem.

The second is the runtime layer. What does the live system actually return? We hit the transcript
endpoint directly in the browser:
read-along-app-production.up.railway.app/transcript/lancedb

The response was immediate and clear: No transcript for lancedb. The live system was returning
nothing. Not an error in the traditional sense — just missing data.

The third is the data layer. What actually exists on disk and in the repository? Running
Get-ChildItem on the backend transcripts folder showed thirty-one JSON files. A comparison
against the fifty-five topics in the dropdown revealed the gap: twenty-five topics had audio
on Google Drive but had never been transcribed. The JSON files simply did not exist.

The karaoke code was perfect. The data it needed had never been created.

---

## The Pipeline Gap Concept

Every system has a pipeline — a sequence of steps that transforms raw input into working output.
When something is missing, the failure is almost never in the middle of the pipeline. It is
usually a step that was skipped entirely.

The read-along app pipeline for adding topics looks like this. First, audio is generated from
vault markdown using the TTS system. Second, audio is uploaded to Google Drive. Third, Whisper
transcribes the audio into word-timestamp JSON files. Fourth, those JSON files are committed
to the repository. Fifth, Railway serves them through the transcript endpoint.

The twenty-five legacy topics had completed steps one and two. Drive had their audio files.
But steps three through five had never happened. There was no tool to download existing Drive
audio back to local staging for transcription. That download step was the missing link.

The solution was building download_legacy.py — a focused script that authenticates to Google
Drive using the same credentials as the backend, reads the drive index, identifies which topics
have path-format entries without corresponding transcripts, and downloads each audio file to
the staging directory. After download, the existing transcribe_batch.py script handled
Whisper transcription automatically. Twenty-five files. Twenty-five transcripts. All fifty-six
topics now have karaoke.

---

## What Was Built and Shipped

Beyond fixing the karaoke gap, this session shipped four major features.

The Knowledge OS tab was transformed from a static iframe into a native vault browser. The
previous implementation embedded an external HTML page inside the app — fragile, not mobile-
friendly, and impossible to interact with. The replacement is a three-level navigator built
directly in React. The first level shows all top-level folders in the BRAIN_OS vault with file
counts. The second level shows the markdown files inside a selected folder, with a search filter.
The third level renders the file content with formatted headings, bold text, inline code,
and bullet lists. Back navigation works at every level. The vault updates automatically because
the backend reads directly from the GitHub repository on every request.

Ask About This Document was added to the content view. When reading any vault file, a question
input appears below the rendered content. Submitting a question sends both the question and
the full document text to the Claude API. The backend skips its normal retrieval-augmented
generation process and uses the specific document as the sole context for Claude's answer.
This means every markdown file in the vault becomes an interactive study resource — not just
readable, but queryable.

Paragraph voice reading was added to all long content blocks. Any paragraph containing five
or more lines, or two hundred and eighty or more characters, receives a speaker button in
its top-right corner. Tapping the button fetches audio from the speak endpoint and plays it
through the browser's audio system. The button turns into a stop indicator while playing.
Tapping it again stops playback immediately. Opening a new file or navigating back also
stops any playing audio automatically.

Voice consistency was unified across the entire application. Previously the Ask tab used the
browser's built-in speech synthesis, which on iOS produces a robotic system voice. All speak
buttons throughout the app now use the same Edge TTS endpoint with the Jenny Neural voice —
a warm, natural female voice consistent with the Kokoro voice used in pre-generated listen
audio. One endpoint, one voice, every tab.

---

## Infrastructure Locked In

Three infrastructure improvements were made permanent this session.

The Vercel auto-deploy connection was confirmed active. The frontend deployment had been
connected to the GitHub repository two days prior, but the manual deploy habit had persisted.
Every git push to the main branch now triggers both Railway for the backend and Vercel for
the frontend simultaneously. The command sequence that ships everything is now: git add,
git commit, git push. Nothing else.

The compile session rebase fix was applied to the session close script. When the remote
repository contains commits that have not been pulled locally, a git push will fail with a
rejection error. The fix inserts a git pull with the rebase flag before every commit step,
synchronizing the local branch with the remote before attempting to push.

The Telegram notification fix was verified working. The send function now strips whitespace
from environment variables on read and validates the chat identifier as a proper integer
before making any API call. A live test confirmed status two hundred — message delivered.

---

## The Cost Model You Need to Understand

Early development sessions were expensive. The root cause was model selection. Claude Opus,
the most capable model in the Claude family, costs fifteen dollars per million input tokens
and seventy-five dollars per million output tokens. Claude Sonnet costs three dollars per
million input tokens and fifteen dollars per million output tokens. Opus costs five times more
than Sonnet for every token processed.

In one early session, Opus consumed eighty-seven percent of the total API bill. A single
session cost nearly eighteen dollars.

After setting claude-sonnet-4-6 as the global default in the Claude configuration file, the
cost per session dropped dramatically. Sonnet is not a lesser model — it is the appropriate
model for the vast majority of development tasks. Opus should be reserved for the most complex
reasoning challenges, not routine code generation and debugging.

The second multiplier is execution efficiency. When Claude has direct access to the file system
through MCP tools, it reads actual files, writes actual fixes, runs actual commands, and catches
its own errors — all within the same turn. Compared to a workflow where every file must be
manually copied and pasted into a chat window, and every command must be retyped by hand,
MCP-enabled sessions consume roughly three times fewer tokens for the same amount of work.

Combined, the right model and the right execution environment produce approximately ten to
fifteen times better value per dollar than early sessions.

---

## Local Development Versus Production

Every application exists in two environments simultaneously. Understanding the difference
between them is foundational to shipping reliably.

Localhost is the workshop. Running npm run dev in the frontend directory starts the Vite
development server at localhost port 5173. Changes to source files appear in the browser
instantly on save. No build step. No deployment. No waiting. Only the developer can see it.

Production is the job site. The live application at read-along-app-psi.vercel.app is what
users see. It runs optimized, built code that Vercel assembled from the source files after
the last git push. Updating production requires a commit and a push.

The correct workflow is to develop at localhost, verify the feature works as expected, then
push to deploy. Pushing directly to production without local verification is the habit that
produces broken features in front of users.

For this application, the backend always runs on Railway regardless of which frontend
environment is active. The frontend source code points to the Railway URL for all API calls.
This means local development uses a live production backend — which is acceptable for this
project's scale, and means local testing reflects real production behavior accurately.

---

## Principles Earned

Every principle in this section was proven through real work completed in this session.

Never debug assumptions. Debug reality. Check the code layer, the runtime layer, and the
data layer before writing any fix. The bug lives where reality diverges from assumption.

Identify pipeline gaps before building solutions. A missing step in a pipeline is not a bug
in the code — it is an absent tool. Build the missing tool, run the existing pipeline, close
the gap permanently.

One command ships everything. After connecting version control to deployment infrastructure,
the only command needed to update both frontend and backend simultaneously is git push.
Every manual step beyond that is waste.

The right model for the right task. Sonnet handles ninety-five percent of development work
at one-fifth the cost of Opus. Reserve expensive models for genuinely complex reasoning, not
routine execution.

Local before production. Build in the workshop. Deliver to the job site. Never skip the
workshop step.

---

This chapter represents a complete cycle of engineering work: diagnosis, root cause analysis,
tool building, feature shipping, and infrastructure hardening — all documented with the
specific commands, commits, and verification steps that prove each principle works.

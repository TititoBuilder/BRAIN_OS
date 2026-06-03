---
knowledge_os_machine_key: function_calling
knowledge_os_domain: AI/ML
knowledge_os_status: Practiced
knowledge_os_score: 70
knowledge_os_priority: High
knowledge_os_evidence: resolve-mcp-server 31 tools
knowledge_os_last_touched: '2026-05-18'
---
# Function Calling

## What It Is
Function calling is how a language model reaches beyond text to actually do
things. You describe a set of functions to the model, what each does and what
arguments it takes, and when answering would require one, the model does not try
to fake it. Instead it outputs a structured request to call that function with
specific arguments. Your code runs the function and hands the result back. It is
the bridge from a model that talks to a system that acts.

## How It Works
You give the model a list of available tools, each with a name, a description, and
a schema for its parameters. When the model decides a tool is needed, it returns a
structured object naming the tool and the arguments it chose, not prose. Your
application detects that, executes the real function, getting live data, hitting an
API, doing a calculation, and returns the result to the model, which then folds it
into its answer. The model never runs the function itself; it only requests the
call, and your code stays in control of what actually executes.

## Why It Matters
This is the mechanism underneath tools and agents, including the MCP servers in
this system. Without it, a model can only describe what it would do; with it, the
model can drive real actions, query your data, control DaVinci Resolve, read your
vault, while you decide which functions exist and validate every call before
running it. That control point matters: because your code mediates every
execution, the model's reach is exactly the set of functions you chose to expose,
no more.

## The Pattern
Describe the tools, let the model request a call with structured arguments, run it
in your own code, return the result. The model decides what to call; you decide
what is callable and what actually runs.

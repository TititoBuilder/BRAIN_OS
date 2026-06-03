---
knowledge_os_machine_key: prompt_engineering
knowledge_os_domain: AI/ML
knowledge_os_status: Mastered
knowledge_os_score: 88
knowledge_os_priority: High
knowledge_os_evidence: All 6 CLAUDE.md files + prompting_architecture audio
knowledge_os_last_touched: '2026-05-24'
---
# Prompt Engineering

## What It Is
Prompt engineering is the craft of writing the input to a language model so it
produces the output you want. Because the model works entirely from the context
you give it, how you frame the request, what you include, what you ask for, in what
form, directly shapes the result. It is less trick and more clear specification.

## How It Works
The reliable techniques are about clarity and context. Be specific about the task
and the desired format rather than vague. Give examples of the input-output you
want, the model generalizes from them strongly. Ask it to reason step by step for
problems that need working-through, which measurably improves accuracy. Provide the
relevant facts in the prompt rather than assuming the model knows your situation,
since it only has what you give it. Assign a clear role or constraints when they
matter. And when you need structured output, say so explicitly and show the shape,
so the result is parseable rather than free prose.

## Why It Matters
The same model gives a mediocre answer to a vague prompt and an excellent one to a
well-constructed prompt, with no change to the model at all. Since the context is
the only lever you have at use time, prompt engineering is the highest-leverage
skill for getting value from a model. It is also what makes outputs reliable enough
to build on: a prompt that demands a specific structure and supplies the needed
facts turns an unpredictable generator into a dependable component in a pipeline.

## The Pattern
Specify clearly, show examples, supply the needed context, ask for reasoning and
for structure when they help. The context is your only lever; pull it
deliberately.

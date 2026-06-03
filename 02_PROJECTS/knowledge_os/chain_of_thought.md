---
knowledge_os_machine_key: chain_of_thought
knowledge_os_domain: AI/ML
knowledge_os_status: Learning
knowledge_os_score: 50
knowledge_os_priority: Medium
knowledge_os_last_touched: '2026-05-05'
---
# Chain of Thought

## What It Is
Chain of thought is prompting a language model to reason through a problem step by
step before giving its answer, instead of jumping straight to a conclusion. By
asking it to show its working, you get both better answers on problems that need
reasoning and a visible trace of how it got there.

## How It Works
The model generates text one token at a time, each new token conditioned on
everything written so far, including its own previous words. When you let it write
out intermediate steps, those steps become part of the context it reasons from, so
each step builds on the last and the final answer rests on actual worked-through
logic rather than a single leap. You trigger it simply, by asking it to think step
by step, or by showing examples that include reasoning, and for hard problems this
measurably improves accuracy compared to demanding the answer immediately.

## Why It Matters
A model forced to answer in one shot has no room to work, it must commit to a
conclusion in its first tokens. Multi-step problems, arithmetic, logic, anything
requiring intermediate deductions, are exactly where that fails. Chain of thought
gives the model space to compute the pieces before combining them, which is why it
is one of the most reliable accuracy boosts in prompting. The visible reasoning is
a bonus: when the answer is wrong, you can often see which step went wrong, making
the model's behavior debuggable instead of opaque.

## The Pattern
For anything needing reasoning, ask for the steps before the answer. The working
becomes context the answer is built on, and a wrong answer shows you where it
broke.

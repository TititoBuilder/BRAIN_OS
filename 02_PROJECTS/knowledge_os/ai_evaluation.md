---
knowledge_os_machine_key: ai_evaluation
knowledge_os_domain: AI/ML
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# AI Evaluation

## What It Is
AI evaluation is how you measure whether a model or AI system is actually doing its
job well, rather than just feeling like it does. It is the discipline of defining
what good output means for your task and testing against it systematically, so you
can tell if a change improved things or quietly made them worse.

## How It Works
You build a set of test cases, representative inputs paired with what a good
response looks like, and run the system against them. For tasks with clear right
answers you can score automatically, did it retrieve the correct document, did the
output parse, did the number match. For open-ended tasks where there is no single
right answer, you use rubrics scored by humans, or increasingly by another model
acting as judge against defined criteria. The essential move is to fix an
evaluation set and rerun it on every change, so improvement and regression become
measurable instead of guessed.

## Why It Matters
Without evaluation, you are flying blind: a prompt tweak or model swap might help
some cases and break others, and vibes will not tell you which. This is acute for
AI because outputs vary and failures are often subtle, an answer that reads fluent
but is wrong. A real evaluation set turns development into engineering, you change
something, rerun the suite, and see the effect, the same way a test suite governs
code. It is what lets you trust that a system is getting better rather than just
different.

## The Pattern
Define what good means, fix a test set, rerun it on every change. Measure
improvement instead of feeling it, because fluent and correct are not the same
thing.

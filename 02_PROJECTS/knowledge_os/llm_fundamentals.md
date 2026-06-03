---
knowledge_os_machine_key: llm_fundamentals
knowledge_os_domain: AI/ML
knowledge_os_status: Learning
knowledge_os_score: 55
knowledge_os_priority: High
knowledge_os_last_touched: '2026-05-20'
---
# LLM Fundamentals

## What It Is
A large language model is a system trained on enormous amounts of text to predict
what comes next, and from that single skill emerges the ability to answer
questions, write, summarize, and reason in language. At its core it is a next-token
predictor; everything it appears to do is built on predicting the most likely
continuation of the text it is given.

## How It Works
The model breaks text into tokens, pieces of words, and for a given stretch of
tokens predicts a probability for every possible next token, then picks one and
repeats. It was trained by being shown vast text with the next token hidden,
adjusting itself until its predictions matched reality. The text it can consider
at once is its context window, a fixed budget of tokens covering both your input
and its output, which is why long inputs get truncated and why what you put in the
prompt matters so much. It has no memory between calls; each request starts fresh
with only what you provide.

## Why It Matters
Understanding the model as a next-token predictor with a fixed context window and
no memory explains its real behavior. It explains why prompts matter, you are
shaping the context it predicts from. It explains hallucination, a confident
prediction is not a check against truth. It explains why you must supply
relevant information rather than assume it knows your situation, and why
retrieval-augmented generation exists, to put the right facts in the context
window. The mental model guides every practical decision about using one well.

## The Pattern
Treat the model as a next-token predictor working only from its context window,
with no memory of its own. Shape the context deliberately, supply the facts it
needs, and never mistake fluent prediction for verified truth.

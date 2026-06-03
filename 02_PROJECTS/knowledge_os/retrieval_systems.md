---
knowledge_os_machine_key: retrieval_systems
knowledge_os_domain: AI Engineering
---
# Retrieval Systems

## What It Is
A retrieval system finds the most relevant items from a large collection in
response to a query. Search engines are retrieval systems. So is the part of
a RAG pipeline that fetches chunks. The job is always the same: given a query
and a haystack, return the few items that matter most.

## How It Works
There are two broad approaches. Keyword retrieval matches the literal words,
fast and exact but blind to meaning, so "car" won't match "automobile."
Semantic retrieval matches by meaning using vector embeddings, so related
ideas score close even with different words. The strongest systems combine
both, called hybrid retrieval, then rerank the top results with a more careful
model to put the best ones first.

## Why It Matters
Everything downstream depends on retrieval quality. In a RAG system, in a
recommendation engine, in your vault search, the model or the user only ever
sees what retrieval surfaced. Garbage in, garbage out applies with full force.
A common metric is recall, did you find the relevant items at all, traded
against precision, how many of what you returned were actually relevant.

## The Pattern
Retrieval is a funnel: cast wide first, then narrow with reranking. Cheap
broad search to gather candidates, expensive precise scoring on the few.

---
knowledge_os_machine_key: semantic_search
knowledge_os_domain: AI/ML
knowledge_os_status: Learning
knowledge_os_score: 45
knowledge_os_priority: High
knowledge_os_evidence: LanceDB BDF vector search
knowledge_os_last_touched: '2026-05-12'
---
# Semantic Search

## What It Is
Semantic search finds results by meaning rather than by matching words. Ask for
how to stop conceding goals and it can surface a document about defensive
organization even though none of those exact words appear. It understands intent
and concept, where keyword search only matches literal text.

## How It Works
Both the query and the searchable content are converted into embeddings, vectors
that represent meaning, and the search finds the content whose vectors are closest
to the query's. Because closeness means similar meaning, related ideas match even
with different vocabulary. The strongest systems combine this with keyword search,
called hybrid search, since keywords still win for exact terms like names, codes,
and IDs that must match precisely, and then rerank the combined top results with a
more careful model to order the best ones first.

## Why It Matters
Keyword search fails exactly where it matters most: when the user does not know
the precise term used in the document, or when the same idea is phrased many ways.
Semantic search closes that gap, which is why it powers modern retrieval and the
search behind RAG systems, including the ASK feature in this system that searches
your notes by meaning. The practical lesson is that pure semantic and pure keyword
each miss cases the other catches, so serious search blends them rather than
choosing one.

## The Pattern
Match meaning, not just words, and blend with keyword search for the exact terms
that must hit literally. Embed query and content alike, find the nearest, rerank
the top.

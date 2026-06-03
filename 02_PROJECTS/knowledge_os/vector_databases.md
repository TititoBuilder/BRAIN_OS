---
knowledge_os_machine_key: vector_databases
knowledge_os_domain: Data Engineering
knowledge_os_status: Practiced
knowledge_os_score: 72
knowledge_os_priority: High
knowledge_os_evidence: 'LanceDB migrated from WD Elements to C: drive'
knowledge_os_last_touched: '2026-05-10'
---
# Vector Databases

## What It Is
A vector database stores data as vectors, lists of numbers that capture meaning,
and finds items by similarity rather than by exact match. Where a normal database
answers where does this field equal this value, a vector database answers what is
most similar in meaning to this. It is the storage engine behind semantic search
and retrieval-augmented generation.

## How It Works
Each piece of content is turned into a vector, an embedding, by a model, and the
database stores those vectors. At query time your search text becomes a vector
too, and the database finds the stored vectors closest to it in space, closeness
meaning similar in meaning. Doing this exactly across millions of vectors would be
slow, so vector databases use approximate nearest neighbor indexes that trade a
tiny bit of accuracy for enormous speed, returning the top matches in
milliseconds. LanceDB, the store in this system, is an example: it keeps the
soccer knowledge documents as embeddings and serves similarity queries locally.

## Why It Matters
This is what makes a model able to search your own knowledge by meaning instead of
keywords. A keyword store cannot tell that goalkeeper and shot-stopper are
related; a vector store can, because their embeddings sit close together. It is
the retrieval half of RAG, the part that finds the right chunks to feed the model,
and the quality of that retrieval largely determines the quality of the answer.
Choosing it well, and indexing it well, is foundational to any system that
searches meaning.

## The Pattern
Store meaning as vectors, search by nearness, use an approximate index for speed.
When you need to find by what something means rather than what it literally says,
this is the engine.

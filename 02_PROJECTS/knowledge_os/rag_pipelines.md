---
knowledge_os_status: Practiced
knowledge_os_machine_key: rag_pipelines
knowledge_os_domain: AI Engineering
---
# RAG Pipelines

## What It Is
RAG stands for Retrieval Augmented Generation. It solves a core problem with
language models: they only know what they were trained on, and they can make
things up. A RAG pipeline fixes this by fetching real documents at question
time and handing them to the model as context, so the answer is grounded in
actual sources instead of memory.

## How It Works
The flow has two halves. First, indexing: you take your documents, split them
into chunks, convert each chunk into a vector embedding, and store those
vectors in a database. This happens once, ahead of time. Second, retrieval:
when a question comes in, you embed the question the same way, find the chunks
whose vectors are closest to it, and feed those chunks to the model alongside
the question. The model answers using what it was just handed.

## Why It Matters
RAG is how you give a general model private or current knowledge without
retraining it. Your Read-Along app's ASK tab is a RAG pipeline: it retrieves
from your own notes, then lets the model answer from them. The quality of a
RAG system lives almost entirely in retrieval. If you fetch the wrong chunks,
even a perfect model gives a wrong answer, because it can only reason over
what it was given.

## The Pattern
Retrieval is the bottleneck, not generation. Most RAG improvements are really
retrieval improvements: better chunking, better embeddings, better ranking.

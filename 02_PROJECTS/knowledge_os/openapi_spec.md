---
knowledge_os_machine_key: openapi_spec
knowledge_os_domain: APIs & Protocols
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: Medium
---
# OpenAPI Spec

## What It Is
An OpenAPI specification is a standard, machine-readable description of a REST API:
every endpoint, what it accepts, what it returns, and how authentication works,
written in a structured format. It is a contract that describes the API precisely
enough that both humans and tools can understand it without reading the source code.

## How It Works
You write the spec as a structured document listing each endpoint, its method, its
parameters and their types, the shape of request and response bodies, the possible
status codes, and the security scheme. Because it is a formal, machine-readable
format, tools do powerful things with it: generate interactive documentation that
lets people try the API in a browser, generate client code in many languages so
consumers do not hand-write requests, and validate that requests and responses
actually match the contract. The spec can be written by hand or generated from the
code, and either way it becomes the single agreed description of the interface.

## Why It Matters
Without a formal spec, an API's behavior lives only in scattered docs and the code
itself, so consumers guess, documentation drifts out of date, and every integration
re-discovers the same details. An OpenAPI spec makes the contract explicit and
single-sourced: documentation, client libraries, and validation all flow from it, so
they stay consistent. It is how an API becomes something others can adopt quickly and
reliably rather than reverse-engineer, and it connects to the REST design principles
by making that design formally checkable.

## The Pattern
Describe the API as a formal, machine-readable contract, then let tools generate
docs, clients, and validation from it. One single-sourced spec keeps everything
about the interface consistent and adoptable.

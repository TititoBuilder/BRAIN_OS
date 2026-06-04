---
knowledge_os_machine_key: federated_systems
knowledge_os_domain: Systems Design
knowledge_os_status: Practiced
knowledge_os_score: 72
knowledge_os_priority: High
knowledge_os_evidence: brain-audio Shared Core pattern
knowledge_os_last_touched: '2026-05-13'
---
# Federated Systems

## What It Is
A federated system splits work between a powerful local node and a lightweight
remote coordinator, each doing what it is best at. Rather than putting everything in
the cloud or everything local, you federate: the heavy computation happens where the
hardware and data are, and a thin remote layer coordinates, stores small state, and
serves results. It is a deliberate division of labor across the boundary between
local and cloud.

## How It Works
The local node is the heavy compute engine, it has the GPU, the large files, the raw
processing power, so the expensive work, generating audio, transcribing,
heavy transformation, happens there at zero marginal cost and zero latency. The
cloud node is a lightweight coordinator: it does not do the heavy lifting, it routes,
stores small artifacts and state, and serves finished results to clients. Work flows
from local to cloud as finished products, the local machine produces, pushes the
small result up, and the deployed app simply serves it. Each side is matched to its
strength rather than forced to do everything.

## Why It Matters
This is the architecture of your own system, and it captures a real insight: there
is no reason to pay cloud prices and latency for compute your local hardware does
better and free, and no reason to expose heavy local machinery to serve simple
remote requests. Federating, local machine as compiler, cloud server as coordinator,
gives you the GPU's power without cloud cost and the cloud's reach without local
exposure. It is why pre-processing locally and pushing finished artifacts up beats
running everything in one place, the right work happens in the right node.

## The Pattern
Put heavy compute on the local node that owns the hardware, and a lightweight
coordinator in the cloud that routes and serves. Match each side to its strength;
produce locally, coordinate remotely.

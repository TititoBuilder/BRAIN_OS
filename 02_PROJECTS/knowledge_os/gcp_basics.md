---
knowledge_os_machine_key: gcp_basics
knowledge_os_domain: Cloud & DevOps
knowledge_os_status: Learning
knowledge_os_score: 35
knowledge_os_priority: Medium
knowledge_os_evidence: Drive API, drive_sync.py
knowledge_os_last_touched: '2026-05-15'
---
# GCP Basics

## What It Is
Google Cloud Platform is Google's suite of cloud services, computing, storage,
databases, and the APIs around them, that you rent and run code against instead of
owning physical machines. For most practical purposes it provides the
infrastructure your applications use: somewhere to store files, run code, and
authenticate access, all reachable through APIs.

## How It Works
Everything in GCP lives under a project, the container that groups your resources,
billing, and permissions. Access is controlled by identity and access management,
where you grant specific permissions to specific identities rather than handing out
broad access. Programs that need to act, like a backend uploading to storage,
authenticate as a service account, a non-human identity with exactly the
permissions it needs, using a credential file or token rather than a personal
login. Each service, storage, compute, the various APIs, is enabled per project and
called through its own API once the right credentials and permissions are in place.

## Why It Matters
Understanding the project-and-permissions structure explains how cloud access
actually works and why credentials are scoped the way they are. The service-account
model is the right way for automated systems to authenticate, a dedicated identity
with least privilege, rather than embedding a personal password, which connects
directly to the secrets-management discipline of keeping those credentials out of
code and in environment configuration. Knowing the basics makes the difference
between cloud access that is secure and scoped versus over-permissioned and
fragile.

## The Pattern
Group resources under a project, grant least-privilege permissions to scoped
identities, and let automated systems authenticate as service accounts. Scope
access tightly; keep credentials in config, never in code.

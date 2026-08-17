---
knowledge_os_machine_key: acid_transactions
knowledge_os_domain: Data Engineering
knowledge_os_status: Learning
knowledge_os_score: 65
knowledge_os_priority: High
knowledge_os_evidence: Learned from gig_tracker SQLite work Aug 15 2026
knowledge_os_last_touched: '2026-08-15'
---

# Lesson 11 — ACID Transactions: What SQLite Promises You

## The Problem ACID Solves

When you write to a database, three things can go wrong:
- Power cuts out mid-write — partial data on disk
- Two processes write simultaneously — data corrupts
- A constraint is violated — database ends up in invalid state

ACID is a set of four guarantees every serious database makes to prevent these.

## The Four Guarantees — From Your Code

Every time you write to gig_income.db:

```python
with _conn() as conn:
    conn.execute("UPDATE cards SET current_balance=55.12 WHERE last4='91009'")
    conn.execute("UPDATE cards SET current_balance=77.95 WHERE last4='4987'")
    conn.commit()
```

### Atomicity — All or Nothing

Both UPDATE statements are one transaction. Either both land on disk, or neither does.
If the app crashes between the two execute() calls — when it restarts,
SQLite rolls back automatically. No partial state. No card 91009 updated
while card 4987 still shows the old balance.

Analogy: A bank transfer. Moving $100 from Account A to Account B is two
operations: debit A, credit B. Atomicity means if the debit succeeds but
the credit fails, the whole thing is undone. Money never disappears.

### Consistency — Rules Always Hold

Before committing, SQLite checks every constraint you defined:
CHECK constraints, NOT NULL, UNIQUE, foreign keys.
If any constraint would be violated, the commit is rejected.
The database moves from one valid state to another valid state — never through
an invalid state.

In gig_tracker: earnings = base_pay + tips is enforced by invariants.py.
Consistency is what makes that check meaningful — the DB can't be written
into a state that violates it if constraints are defined.

### Isolation — Other Connections See Nothing Until Commit

Before conn.commit():
- Your connection sees the new balance
- Every other connection (web.py, gig.py, prop22.py) still sees the old balance

After conn.commit():
- Everyone sees the new balance simultaneously

This is why three scripts can share gig_income.db safely:
web.py reading cards while balance.py is mid-update sees a consistent
snapshot, never a half-written row.

SQLite isolation: file-level locking. One writer at a time.
Only matters at scale — for personal use, it is never a problem.

### Durability — Committed Means Permanent

Before conn.commit(): data is in RAM only.
Power cut = update is gone. Never happened.

After conn.commit(): data is on disk.
Power cut = update survives. Permanent.

conn.commit() is the exact moment data crosses from RAM to disk.
This is why session_close.py always commits before exit —
and why the BRAIN_OS tool contract uses exit codes:
the caller needs to know commit succeeded before moving on.

## The Schema Mismatch Crash — ACID In Action

Error you saw on Render:
  sqlite3.OperationalError: no such column: due_day

Render had an old copy of gig_income.db without the due_day column.
web.py expected it (Consistency violation — schema didn't match code).
The DB rejected the query — it could not move to a valid state.
This is Consistency working correctly: refusing an operation that
would violate the expected schema contract.

Fix: run the migration (ALTER TABLE cards ADD COLUMN due_day INTEGER)
on the Render DB so schema matches code. Or run it automatically on startup.

## The Pattern

```python
with _conn() as conn:          # open connection
    conn.execute("...")         # stage changes in RAM (not on disk yet)
    conn.execute("...")         # stage more changes
    conn.commit()              # ACID guarantee: all land on disk or none do
                               # after this line: Durable, Consistent, Isolated, Atomic
```

The context manager (with _conn()) also handles rollback automatically
if an exception is raised before commit(). You get Atomicity for free.

## Connected to Your Projects

| Concept | Where in gig_tracker |
|---|---|
| Atomicity | balance.py — two card updates in one commit |
| Consistency | invariants.py — enforces earnings = base_pay + tips |
| Isolation | web.py + gig.py + balance.py sharing same DB safely |
| Durability | conn.commit() in every write script |
| Schema mismatch | Render crash — due_day column missing |

## Vault Cluster

Sits with: data_modeling.md (structure) → lesson_11 (guarantees) → database_sharding.md (scale)
Reading order: model it → guarantee it → scale it.


<!-- auto-ingested 2026-08-16 -->
Built from gig_tracker SQLite work during 2026-08-16 session. Covers ACID transaction fundamentals derived from practical database operations in the gig_tracker project.

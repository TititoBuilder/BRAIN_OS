---
type: schema
enforces: "[[Cristian_Principles]]"
status: active
created: 2026-09-09
---
# Ontology

## The rule
An ontology is a taxonomy PLUS the relationships between types PLUS the rules
governing those relationships. Not just categories — categories and how they
connect. A taxonomy tells you what kind of thing something is. An ontology tells
you what that thing may do, what it depends on, and what governs it.

The vault already had the parts and no word for the whole: [[Domain_Taxonomy]]
is a taxonomy, [[Taxonomy_Decision]] is a rule about two taxonomies,
[[BRAIN_OS_Vocabulary]] is the shared language. This note is the layer above them.

---

## The three concepts this ties together

### Taxonomy — a hierarchy of "is-a" types
BUILD / ACT / RECONCILE are three types of Task. `01_DOMAINS` names five fields.
A taxonomy alone is silent about how its types relate to each other or to
anything outside itself. That silence is the gap an ontology fills.

### Provenance — how strongly a fact is evidenced
A property carried by the fact itself, not by the table it sits in.

The worked example is gig_tracker's **balance tables** — `cards`,
`cash_accounts`, `debts` — which carry two provenance columns added 2026-09-06
by `migrate_provenance_2026.py`:

- `source` — where the value came from
- `last_refreshed` — when the value was TRUE in the real world, which is not
  `updated_at` (when the row was written). A statement dated the 14th entered
  on the 22nd has an eight-day gap between those two, and that gap is the whole
  reason the column exists.

The ladder, most authoritative first:

    statement > web > export > manual > seeded

Five values, and the ordering is load-bearing — it is what lets code tell a
downgrade from an upgrade without a human judging each case.

**`is_hypothetical` is not on this ladder.** It is a separate boolean on
`debts`, marking modelled financing structures that are not money owed at all.
Evidence strength and "is this real" are different questions; two seeded
placeholder loans were counted as real debt for months precisely because
nothing distinguished them. Do not fold one axis into the other.

**The coarse view, generalized 2026-09-09:** every Fact is **Confirmed** or an
**Assumption**, and the cut is *authorship*, not recency or precision.

| | |
|---|---|
| `statement` \| `web` \| `export` | **Confirmed** — an institution produced the number, whatever the capture method |
| `manual` \| `seeded` | **Assumption** — a human asserted it, however plausible |
| NULL | **Unknown** — nobody recorded a source; never Confirmed by default |

A screenshot of a bank's own balance page is weaker *evidence* than a PDF
statement — that is what the ladder is for — but the bank still authored the
number. A figure typed from memory is a different kind of thing entirely,
however fresh. The coarse view sits on top of the ladder; it never replaces it.

The rule that comes with it: an Assumption never silently becomes a Confirmed
fact (see [[Cristian_Principles]]).

The proof was already written down before the rule was named. `engaged_miles`
is synthetic — Spark never reports engaged mileage, so rows were filled by
multiplying hours by an assumed constant. Calibrating against that column
re-reads the assumption and calls it agreement. Ten rows currently sit on the
constant. The only valid method is payment inversion, which never reads the
miles column at all. An Assumption that loses its label becomes
indistinguishable from evidence, and every calculation downstream inherits the
false confidence.

### Orthogonality — two systems that answer different questions
Two classification systems are orthogonal when they answer different questions
about the same thing and neither implies the other. They do not nest, and
forcing them to nest destroys one of them.

The vault's own case is [[Taxonomy_Decision]]: the 5-layer architecture
encyclopedia (`01_DOMAINS`) answers "what kind of engineering is this?", while
the 9 learning domains answer "what topic do I want to listen to?". Both kept,
deliberately, because collapsing them would destroy a lens in active use.

Same shape one level up: the four-bucket routing in `00_INDEX`
(CONTENT / BUSINESS / OPERATIONS / PERSONAL) answers "which project domain",
while BUILD / ACT / RECONCILE answers "who executes this". A gig_tracker task is
OPERATIONS and BUILD at once. The axes do not collide because they are not
measuring the same thing.

**The test:** if a thing can hold a value on both axes at once without
contradiction, the axes are orthogonal — keep both. If one value forces the
other, one axis is redundant — collapse it.

#### The negative case: shared vocabulary does not imply shared ontology
Orthogonality is two names for two real axes. The failure mode is the mirror
image — **one name over several unrelated axes**, which looks like a shared
concept and is not.

gig_tracker has four tables with a column literally named `source`:

| Column | What it actually says |
|---|---|
| `pay_periods.source` | which platform — `Spark` \| `Roadie` |
| `delivery_runs.source` | the row's lifecycle stage — `xlsx_import`, `estimated`, `superseded`, … |
| `platform_statements.source` | how the statement was obtained — includes `derived_zero` |
| `cards` / `cash_accounts` / `debts.source` | evidence authority — the ladder above |

Zero shared meaning. Only the last is a provenance ladder. `superseded` on
`delivery_runs` does not mean *weakly evidenced*, it means *replaced by a real
import*; `estimated` there is a lifecycle stage awaiting the real XLSX, not a
confidence level. Mapping either onto Confirmed/Assumption is a category error
that would put a meaningless label on real data.

This is a naming collision masquerading as a shared concept — the opposite
error from collapsing two orthogonal axes, and harder to see, because the
shared column name actively invites the mistake. **Shared vocabulary does not
imply shared ontology.** The check is to ask what question each column answers,
not what it is called.

---

## The working ontology (as of 2026-09-09)

### Classes
| Class | Distinguishing property |
|---|---|
| Project | the thing being built |
| Task | `type`: BUILD \| ACT \| RECONCILE |
| Fact | `evidence`: Confirmed \| Assumption |
| Decision | rests on Facts, dated |
| Concept | reusable across Projects |
| Principle | earned, governs Tasks |

### Relationships
    Project    contains   Task
    Task       produces   Fact
    Decision   depends on Fact
    Principle  governs    Task
    Concept    applies to Project

A Decision that depends on a Fact inherits that Fact's evidence status. This is
why provenance is a property of the Fact and not of the store it lives in — the
status has to travel with the fact through every derivation.

---

## Status
BUILD / ACT / RECONCILE is new vocabulary as of this date and appears nowhere
else in the vault yet.

Confirmed / Assumption is further along: gig_tracker implemented it the same
night in `tracker/evidence.py`, as a computed view over the existing `source`
ladder with the five values and their ordering unchanged. The write guard is a
SQLite trigger per balance table rather than a check in the CRUD helpers,
because every balance edit in that repo's history was made by a one-off script
writing raw SQL — a guard the writers bypass is not a guard. On any write that
lowers evidence rank, the replaced value and its provenance are appended to an
`evidence_ledger`. It preserves; it does not block.

Adoption elsewhere — other projects, and vault notes that state financial or
factual claims — is not done.

**Origin session:** gig_tracker / van-financing work, 2026-09-09.

---
**→** [[Cristian_Principles]] · [[Taxonomy_Decision]] · [[Domain_Taxonomy]] · [[BRAIN_OS_Vocabulary]] · [[00 Gig Tracker MOC]]

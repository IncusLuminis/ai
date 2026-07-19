# Orchestration Model

**Status:** Draft / Proposed
**Applies to:** the six roles in `./README.md`

## 1. The standard flow

```text
Spec / PRD / feature request
        |
        v
 [Product_Owner]  decomposes into Epic + Stories
        |            (Project 1 for product work,
        |             Project 2 for agent-team/process work)
        v
   Story: Status = Ready
        |
        v
    [Coder]  claims Story -> Status = In Progress
        |    creates/refreshes own working branch off latest main
        |    implements, commits only to that branch
        v
   Opens PR -> Status = In Review
        |
        v
  [Validator]  reviews: acceptance criteria, tests, lint,
        |      security-review / review skills as applicable
        |
        +-- changes requested --> back to [Coder], Status = In Progress
        |
        v
   Approved, awaiting human merge approval
        |
        v
  Human (Mihal) approves merge into main
        |
        v
    [DevOps]  CI checks, environment promotion, staging/prod rollout
        |
        +---> if binary/media assets involved:
        |         [Media_keeper] optimizes, stores, publishes to CDN,
        |         returns canonical URL(s) back onto the issue
        |
        v
  [Publisher]  ships finished, validated content/feature externally
        |      (blog post, social post, PDF/document, release notes)
        v
  [Product_Owner]  closes the Story, rolls status up to the Epic,
                    reports progress
```

Not every Story touches every role — a pure infra Task may only involve `DevOps`; a copy-edit-only content change may only involve `Product_Owner` and `Publisher`. The flow above is the superset.

## 2. Board status ownership

Who is allowed to move a card between which statuses:

| Status | Entered by | Notes |
|---|---|---|
| Backlog | `Product_Owner` | Created from spec decomposition |
| Ready | `Product_Owner` | Acceptance criteria + Size/Estimate set (Definition of Ready met) |
| In Progress | `Coder` or `DevOps` | Whoever claims the work; Start date set |
| In Review | `Coder` (on opening PR) | Handed to `Validator` |
| Blocked | any role | Must leave a comment explaining the blocker; `Product_Owner` triages |
| Done | `Product_Owner` | Only after `Validator` approval + human merge + (if applicable) `Media_keeper`/`Publisher` confirmation |

## 3. RACI

R = Responsible, A = Accountable, C = Consulted, I = Informed. Human (Mihal) is always Accountable for merges to `main` and for publishing to public channels — no agent merges or publishes unsupervised by default.

| Activity | Product_Owner | Coder | Validator | DevOps | Publisher | Media_keeper | Human |
|---|---|---|---|---|---|---|---|
| Spec decomposition / Epic-Story authoring | R/A | I | I | I | I | I | C |
| Code implementation | I | R/A | I | C | — | — | I |
| QA / review gate | I | C | R/A | I | — | — | I |
| CI/CD, environments, infra scripts | I | C | I | R/A | I | I | I |
| Media/asset preparation + CDN | I | C | — | C | C | R/A | I |
| Publishing (blog/social/PDF) | I | — | I | I | R/A | C | A |
| Merge to `main` | I | R | C | I | — | — | A |
| Progress reporting | R/A | I | I | I | I | I | I |

## 4. Branch and repo discipline (proposed org-wide default)

Every repo in the portfolio is its own git repository (see the top-level layout: `products/*`, `shared/*`, `platform/*`, `tools`, `docs`, each with its own `origin`). `products/nebulacast/nebulacast-app/Claude.md` already documents a strict branch policy for that one repo. This design proposes making that the **default for every repo any agent touches**, not just nebulacast-app:

- Start every task from an up-to-date `main`.
- Work only in a dedicated branch for that task; never commit to `main` or to another agent's/human's branch.
- Open a PR back to `main`; merge only after `Validator` approval **and** explicit human sign-off.
- One branch per logical task, not one long-lived branch per agent — avoids stale/conflicting state across unrelated Stories.

This is flagged as an open decision in `implementation-roadmap.md` — it should be written once into `platform/standards` rather than copy-pasted per repo, but that edit is out of scope for this design pass.

## 5. Cross-role boundaries worth naming explicitly

A few boundaries came up repeatedly while drafting the individual charters and are worth stating once, centrally, instead of six times:

- **Coder vs DevOps**: Coder owns application/product code inside a product repo; DevOps owns pipelines, environments, and cross-repo tooling (`tools`, `repo-template`, `platform/workflows`, `.github/workflows` in every repo). A Story that needs both gets split, or DevOps hands Coder a working local environment first.
- **DevOps vs Media_keeper**: DevOps can own *where* media infrastructure lives (e.g. provisioning/config of Cloudflare R2 buckets), but `Media_keeper` owns the *lifecycle* of what's in them — ingestion, format/compression standards, naming, versioning, dedup, publishing to CDN.
- **Publisher vs Media_keeper**: Publisher never uploads raw media itself — it consumes canonical CDN URLs that `Media_keeper` has already produced and validated.
- **Product_Owner vs everyone**: Product_Owner never implements, reviews code, or publishes. Its outputs are always issues/specs/reports, never commits.

# Proposed New Roles (Product_Owner Portfolio Survey)

**Status:** Proposal — not built, not approved.
**Requested:** 2026-07-20, by Mihal ("пусть Product Owner пробежит по всем репозиториям и даст предложения").
**Method:** Read across `products/*`, `platform/*`, `shared/*`, `docs`, `exploration/*` — no code changed, no boards touched. This is the kind of gap-analysis `Product_Owner` is meant to do; done directly this pass rather than dispatched as a separate Claude Code session.

## 1. What the portfolio actually is

Six original roles (`Product_Owner`, `Coder`, `Validator`, `DevOps`, `Publisher`, `Media_keeper`) were designed around **software delivery**: spec → backlog → code → review → ship. Looking across the whole portfolio, a large and growing share of the actual work isn't software delivery at all — it's **content production**:

| Property | Repo(s) | Domain |
|---|---|---|
| NebulaCast | `products/nebulacast/*` | Podcast/media production pipeline |
| Roads of Times | `products/roadsofttimes/*` | Historical content |
| Stellar Attractor | `products/stellar-attractor/*` | Hard sci-fi episodic media (scripts, storyboards, VFX prompts) |
| Visualization Studio | `products/visualization-studio/*` | Software product (the one exception — this is genuinely code) |
| Photomaps | `products/Photomaps` | Geo/photo processing pipeline (notebooks) |
| RSS Reader | `products/RSS_reader` | Flutter mobile app (also genuinely code) |

Three of six product lines are primarily **written/narrative content**, not code. None of the six existing roles owns *writing* prose — `Product_Owner` specs it, `Publisher` ships it once done, but nobody drafts it, translates it, or copy-edits it. That's the actual gap, not a hypothetical one — `stellar-attractor-content`'s `productions/` tree is present but empty (all `.gitkeep`), waiting for exactly this kind of work.

## 2. Proposed roles

### Content_Writer
**Gap:** Drafts the actual scripts/episodes/posts inside a production unit (`editorial/synopsis`, `editorial/script`, `editorial/dialogue` per `stellar-attractor-content`'s production-unit template) — nobody currently does this. `Product_Owner` breaks a season into Stories; `Content_Writer` is who actually writes episode 5.
**Boundary:** Does not decide what gets made (`Product_Owner`) or publish it (`Publisher`); writes drafts against a brief, revises on `Editor` feedback.

### Editor
**Gap:** Prose equivalent of `Validator` — right now nothing checks a script/post for continuity, tone, factual consistency with established canon, or plain writing quality before `Publisher` ships it.
**Boundary:** Reviews and requests changes, doesn't write from scratch. Owns `universe/canon/` consistency for narrative properties (a script contradicting established lore is exactly this role's job to catch, the same way `Validator` catches a PR breaking a contract).

### Translator
**Gap:** Content already mixes Russian and English in the same production (the Episode 4 storyboard has Russian dialogue lines with English shot descriptions) — there's no defined owner for keeping any given piece consistently bilingual, or for localizing site copy.
**Boundary:** Translates/localizes existing approved content; doesn't originate it.

### Copywriter
**Gap:** Distinct from `Content_Writer` — short-form, conversion-focused text (site taglines, social captions, episode blurbs, thumbnails/titles) rather than long-form narrative. Different skill, different brief, easy to under-scope if folded into `Content_Writer`.
**Boundary:** Marketing/promotional text only; doesn't touch the narrative script itself.

### Domain_Consultant (pattern, not a single role)
**Gap:** `stellar-attractor`'s existing storyboard already leans on real orbital mechanics ("Keplerian motion," specific collision-probability numbers, spectral references) — getting the science-flavored details right (or deliberately, consistently wrong) needs a subject-matter check `Content_Writer` alone won't reliably provide. Same pattern would apply to **Roads of Times** (a historian/fact-checker for historical accuracy).
**Concretely:** propose **`Astrophysicist`** now, for Stellar Attractor specifically, as the first instance of this pattern — narrow scope (fact-check/ground technical content on request), not a general science-answering bot.
**Boundary:** Advisory only — reviews and suggests, doesn't write dialogue or make narrative calls.

## 3. Not proposed (considered, rejected)

- **Separate roles per product** (e.g. `NebulaCast_Writer`, `RoadsOfTimes_Writer`) — the skill (writing a script, editing prose) is the same regardless of which property; scope by assignment (which production, which repo) the same way `Coder` already isn't split per-product.
- **A general "Researcher" role** — `Domain_Consultant` covers the narrow, on-request fact-check need; a standing open-ended research role has no clear boundary and risks duplicating what `Product_Owner` already does when reading specs.

## 4. Suggested sequencing

Don't build all four at once. `Content_Writer` first — it's the actual bottleneck (empty `productions/` trees waiting for scripts). `Editor` second, as soon as `Content_Writer` produces something to review — mirrors why `Coder` shipped before `Validator` had real PRs to look at. `Translator` and `Copywriter` on demand, once there's real bilingual/marketing work queued. `Astrophysicist` (and any later `Domain_Consultant` instances) whenever a specific production actually needs a science/history check, not speculatively.

## 4a. 2026-07-21 update: finalized as a broader roster

Mihal turned this into a concrete list, broader than the four roles proposed above and named differently in places — see the Roster table in `README.md` for the current, authoritative set (`Content_Master`, `Media_keeper`/"Media Librarian", `Studio_Visualizer`, `Content_Translator`, `Fellow_Astrophysicist`, `Fellow_Historian`, `Publisher`/"Fellow Publisher", `Incus_Designer`). Notes on the delta from this document's original proposal:

- `Content_Writer` and `Copywriter` are superseded by the single, broader `Content_Master` — one role owns all text content rather than splitting long-form from short-form.
- `Editor` carries over as `Content_Editor` (2026-07-21: reinstated, initially left out of the first pass of this update) — reviews `Content_Master` and `Content_Translator` output for style, clichés, and readability against a shared house linguistic rule set, same "prose `Validator`" boundary as originally proposed.
- `Translator` and the `Astrophysicist` `Domain_Consultant` instance carry over unchanged.
- `Historian` (floated in §2 above as "same pattern would apply to Roads of Times") is now a first-class proposed role, not just a hypothetical.
- `Studio_Visualizer` and `Incus_Designer` are new — no counterpart in the original four-role proposal.

None of the `Proposed` rows are built yet; still not built, not approved.

## 5. Relationship to the Stellar Attractor character personas

Separate from this functional-role proposal: Mihal is also standing up **named, in-universe personas** (Brown, Kellan, Marchand, ...) as their own Slack presences with distinct personalities, grounded in the existing Stellar Attractor canon (`legacy/Episode 4/Story board.csv` and related notebooks). See `products/stellar-attractor/stellar-attractor-content/universe/characters/`. These are a different kind of thing from the functional roles above — chat companions in character, not production-pipeline workers — though nothing stops a persona (e.g. an in-character "Astrophysicist" who happens to also be a named character) from eventually doing both.

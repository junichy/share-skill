# LSI/PAA Keyword Discovery

Use this reference before article planning, island design, or related-query expansion.

## Core Principle

Keyword discovery is LSI/PAA/tree-first, not bulk keyword-list-first.

Use LSI/PAA/tree data to read how the searcher's intent branches into anxieties, comparisons, conditions, definitions, next actions, and question-support needs. Use bulk search volume only as an annotation layer for known candidates or exact-variant checks. Do not let a flat volume list decide the island, parent/child relationship, or writing order.

## Inputs

Use the project's approved keyword source first, following [keyword-source-research.md](keyword-source-research.md). Combine LSI/PAA
with suggestions, related questions and simultaneous-ranking queries as needed;
preserve each source label. AI-generated suggestions are hypotheses, not observations.

- seed query or seed topic
- target site, audience, service/product fit, and excluded areas
- existing article ledger or URL inventory when available
- LSI/PAA/tree capture from the selected keyword tool
- volume, difficulty, or competition metrics when available
- GSC query/page evidence when working on existing content

## Evidence Labels

Keep evidence labels visible in research and planning artifacts.

- `lsi`: related phrase from an LSI surface
- `paa`: question from a PAA surface
- `tree_path`: branch position in a tool-provided tree
- `related_search`: related search surface
- `bulk_volume`: row discovered only from a flat volume list
- `gsc`: existing query/page evidence
- `manual`: agent or user hypothesis that still needs evidence

Do not collapse these into a generic "related query" label. A PAA-only question can be useful, but it is usually answered in the relevant H2/H3 or checked for ownership before it becomes a standalone article. Do not create an FAQ section solely to collect PAA wording.

## Procedure

1. Define the seed, audience, and site-fit boundary.
2. Capture the LSI/PAA/tree view for the seed. Record source tool, capture date, result URL or id when available, country/language settings, and volume period when shown.
3. Preserve exact query text. Do not merge spaces, notation variants, or near-duplicates unless the artifact records the merge candidate explicitly.
4. Walk the tree by intent branch, not by volume rank. Name each branch with the search noun and intent, such as `営業インターン きつい・不安`, not vague labels such as `悩み`.
5. For each branch, classify the role: `parent hub`, `focused child`, `sibling`, `question support`, `mention`, `hold`, or `drift`.
6. Add volume as an annotation. Treat `0` as known zero and `unknown` as not collected.
7. Stop expanding a branch when it drifts outside the site, repeats the same intent, only produces low-evidence question rows, or would require article-production SERP checks to decide safely.
8. Build one planning tree, not a flat plan plus a separate tree.
9. Before writing any concrete article, run [serp-ownership-check.md](serp-ownership-check.md), then the normal article evidence gates.

## Planning Tree Columns

Use project-local column names when a project already has a contract. Otherwise include these fields in the research artifact or planning table:

- `island`
- `branch`
- `query`
- `source_label`
- `tree_path`
- `volume`
- `intent_role`
- `site_fit`
- `owner_candidate`
- `deep`
- `mention`
- `exclude`
- `next_action`
- `evidence_note`

## Decision Rules

- Broad parent query: create a hub or parent skeleton only when the site needs an entrance page. Do not make it a full encyclopedia before child ownership is known.
- Focused child: consider standalone only when intent is narrow, action is close, and the query can own a URL without blurring another article.
- Sibling: separate only when the branch points to a different next action, audience, comparison axis, timing, or page type.
- Question support: answer in the owner article's relevant H2/H3 unless volume, source strength, and later SERP ownership checks prove standalone demand. Do not force a separate FAQ section.
- Mention: keep short and link to the owner article when one exists or is planned.
- Hold: mark when source evidence is weak, site fit is poor, or SERP ownership must be checked later.
- Drift: exclude when the branch leaves the site purpose, product/service scope, or audience.

## Bulk Volume Rule

Bulk keyword research is not the discovery surface for topic architecture.

Allowed uses:

- annotate exact candidates already found through LSI/PAA/tree
- catch high-volume exact variants that the tree missed
- check whether a branch has enough demand to prioritize ownership checks

Disallowed uses:

- sorting the article plan by volume alone
- creating islands from a flat keyword export
- treating volume-only rows as article targets
- merging exact variants silently to inflate opportunity

## Article Handoff

When handing discovery to article production, include:

- selected island and branch
- target query and nearby queries
- evidence labels and tree paths
- exact volume values and unknown/zero distinction
- owner candidate, `deep / mention / exclude`
- unresolved ownership checks

This discovery phase does not replace article production evidence. For title, outline, writing, rewrite, or diagnosis decisions, keep the existing SERP top 10, title comparison, structure comparison, rank ladder, and 20-30 fallen-page checks.

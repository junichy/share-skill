# SERP Ownership Check

Use this reference after LSI/PAA/tree-first discovery has produced a planning tree and before writing the first article in a dense island.

The goal is not to create another plan. The goal is to prevent cannibalization by deciding which URL owns which nearby query, then reflecting that decision back into the research files and planning tree.

## Trigger

Run this check when any of these are true:

- the user says to start writing from a planning tree
- the first island contains overlapping anxiety, timing, selection, pay, or search-method queries
- a planned new article has an existing owner candidate in the ledger
- a row says `検索結果確認`, `新規記事`, or `リライト` but the nearby queries may overlap

For dense islands, the first task is ownership confirmation, not drafting.

## Inputs

Gather these before opening the article editor:

- planning tree rows for the first island
- existing ledger rows: slug, liveURL, title, parent slug, publish status
- LSI/PAA planning tree, local cluster map, or project inventory if available
- target query and 2-5 nearby query candidates
- likely deep / mention / hold queries from the planning tree

If the project uses a live spreadsheet ledger, treat that live file as authoritative unless project rules say otherwise. Local CSV/XLSX files are snapshots unless explicitly made canonical.

## SERP source

Start with the approved keyword source following [keyword-source-research.md](keyword-source-research.md). Compare queries
under matching source/settings/time windows. Use Google UI only for claims that
require the actual screen; label supplemental evidence separately.

## Procedure

1. Read the first island from the planning tree.
2. Use volume, branch strength, source strength, and site fit to decide which queries deserve ownership checks first.
3. Identify the first article candidate and existing owner candidates.
4. Retrieve the target query in the approved keyword source and record organic top 10, excluding ads, AI Overview, PAA, image/video packs, and duplicate sitelinks from organic rank.
5. Search the existing owner query and the nearby sibling queries.
6. Compare overlap and intent, not just titles.
7. Combine source-labelled SERP evidence with volume, source strength, branch strength, and existing-owner fit.
8. Decide per query:
   - `new focused child`
   - `rewrite existing`
   - `add section`
   - `mention only`
   - `hold`
   - `move to another island`
9. Write a research file under the project's dated research folder.
10. If the decision changes the visible plan, update the planning tree rows and any local generator/script that would otherwise recreate the stale decision.
11. If the project uses a live Google Sheet planning tree, write the same decision back to the live sheet and read back the edited rows.
12. Only then proceed to top10 structure analysis for the article to be written.

## Planning Signals Before SERP Retrieval

Use the LSI/PAA planning tree to decide what to inspect, not to decide the article owner by itself.

Practical interpretation:

- `volume high + branch/source strength high`: important query. Always run SERP evidence ownership check before writing.
- `branch strength high + intent narrow`: likely concentrated intent. Candidate for an owner article or a strong section.
- `branch strength high + source-labelled SERP overlap high`: likely same ownership area. Consider existing owner retarget, integrated rewrite, or section ownership.
- `branch strength high + source-labelled SERP overlap low`: likely independent intent. Consider focused child or sibling article.
- `parent-like tree position + intent broad`: exploration query. Do not rush into a first article; inspect subqueries and page type.
- `volume low + branch strength high`: useful support query. Usually answer it in the relevant H2/H3 or a deep section before considering a standalone article; do not add an FAQ heading by default.
- `volume high + parent-like tree position`: broad hub. Confirm page type in the retrieved results before making it a parent article.
- `volume low + source strength low`: low priority. Usually mention, hold, or capped.

Planning-tree signals explain query importance and relation shape. source-labelled SERP explains current Google ownership. Use both.

## Ownership Decision Rule

Do not decide from query wording alone. Also do not apply a blanket "integrate high-overlap queries" rule.

For each near query set, decide from this combination:

- `volume`: demand size and opportunity cost
- `source strength`: whether the query came from LSI, PAA, tree path, GSC, bulk volume, or manual inference
- `branch strength`: whether the same branch contains multiple close queries and a real searcher concern
- `SERP evidence URL overlap`: shared organic top10 URLs between target and neighbor queries
- `SERP evidence title/H1 overlap`: whether top pages intentionally cover both phrases
- `SERP evidence page type`: article, Q&A, category/listing, tool, official, forum, local page
- `answer overlap`: whether the immediate answer and next action are the same
- `existing owner fit`: whether an existing URL can own the query without breaking its topic

Only split into a `new focused child` when source-labelled SERP shows separable ownership: different URLs or page types are winning, the searcher's next action is different, and adding the query to an existing article would blur the article's main job.

Use `rewrite existing` or `add section` when source-labelled SERP shows shared ownership and an existing URL can naturally absorb the target query. This is a result of the evidence, not a default preference.

## Overlap Heuristic

Use overlap as a guardrail, not a calculator:

- 6+ shared top10 URLs: usually requires a strong reason to split; inspect existing owner fit first
- 3-5 shared URLs: ambiguous; split only when page type, answer, and next action are clearly different
- 0-2 shared URLs: likely independent, but still confirm page type, answer, and existing owner fit

Also consider SERP type. A Q&A-heavy SERP, list SERP, category/listing SERP, or timing/year SERP may need a different owner even when some URLs overlap.

## Research File Shape

Save a concise file such as:

```txt
seo/research/YYYY-MM-DD/<topic>-ownership-check.md
```

Recommended sections:

```md
# <Topic> SERP所有権確認

- date:
- repo:
- source plan:
- live ledger:
- observation method:
- Source / feature / reference / captured time:
- Engine / country / language / device / rank range:
- Google screen context (only if observed):

## 対象範囲

## SERP観察

### <query>
- observed URL:
- organic top results:
- SERP modules:
- notes:

## SERP overlap / ownership判断

| query | ownership decision | owner slug | 理由 |
| --- | --- | --- | --- |

## SERP所有権確認

- target query:
- checked existing URLs:
- checked neighbor queries:
- ownership decision:
- owner slug:
- deep:
- mention:
- exclude:
- cannibal risk:
- why this can proceed:
- unresolved checks:
```

If `unresolved checks` contains evidence needed for ownership, do not draft. Continue SERP checks.

## Planning Tree Feedback Loop

Do not leave the planning tree contradicting the ownership research.

After the research decision:

- change `処理` from `新規記事` to `追記` when a query should not be standalone
- change `階層` from `記事候補` to `深掘り` / `言及` / `保留` when appropriate
- move a query to the correct island when SERP proves the island was wrong
- update `親/吸収先slug`
- update `次アクション`
- update `メモ` with `SERP確認済み`
- if a local generation script controls the CSV/Sheet, update that script too
- update the live spreadsheet if it is the active operational view
- read back the edited rows

If script-based Google Sheets sync fails because of auth/scope, use the available Google Sheets connector if present and report the auth issue clearly. Do not claim full sync when only selected rows were patched.

## Stop Conditions

Stop before drafting when:

- target and existing owner SERPs were not checked with source-labelled results
- the existing ledger owner is unknown
- the plan tree still says `新規記事` for a query the research says should be `追記`
- deep ownership overlaps across two planned articles
- `unresolved checks` contains ownership-critical work

# Parent / Child Topic Classifier

Use this before deciding title, outline, rewrite scope, internal links, or whether to split an article. The goal is not to label a keyword for its own sake. The label changes the required SEO move.

## Classification Labels

- `parent`: the query expects a representative answer page that covers the topic broadly and naturally contains several child anxieties.
- `child`: the query expects a focused answer to one narrow anxiety, material, symptom, location, timing, comparison, or action.
- `mixed`: the SERP contains both broad parent pages and focused child pages, or Google is testing multiple interpretations.
- `unknown`: evidence is insufficient. Do not draft or make a title-only rewrite from this state.

## Evidence To Gather

Judge from the SERP and, for published pages, GSC. Do not judge only from search volume or keyword length.

- SERP breadth: do top 10 pages answer a broad topic, or mostly one narrow question?
- Rank ladder: as pages climb from 10 -> 1, do they broaden into a representative guide, or get more exact to the narrow query?
- Fallen-page comparison: are similar narrow pages stuck around 20 -> 30 because they are child-topic pages for a parent query?
- Page titles and H1s: do winners use broad topic language, or exact child modifiers?
- H2/H3 coverage: do winners include multiple child sections inside one page?
- SERP features: AIO, PAA, videos, images, and snippets often reveal whether Google is summarizing a broad issue or one exact action.
- Query variants: do variants like symptoms, timing, cost, examples, or danger signs appear as sections inside winners or as separate ranking pages?
- GSC query spread: for a published URL, does it get impressions for the parent query, only child queries, unrelated queries, or almost nothing?
- Existing cluster: is there already a stronger parent hub that this page should support instead of replacing?

## Decision Rules

Classify as `parent` when most of these are true:

- top results are broad guides, hospital/official/major-media pages, or category-like resources
- top pages cover definitions, danger signs, what to do, when to contact, common examples, and prevention or next steps
- child queries are handled as H2/H3 sections inside winners
- rank 1 looks like the representative answer, not merely one exact subtopic page
- exact child pages appear lower or only win for more specific modifiers

Classify as `child` when most of these are true:

- top results answer one concrete narrow question first
- titles/H1s repeatedly include the exact modifier
- winners do not need a broad primer before answering
- broader parent pages are absent, lower, or only supplementary
- PAA and snippets focus on the same narrow action, symptom, item, or timing

Classify as `mixed` when:

- top 10 is split between parent and child pages
- rank bands change interpretation, such as 1-3 broad and 4-10 narrow
- the target query is short but the SERP is currently unstable or feature-heavy
- GSC shows child-query impressions but little or no parent-query exposure after indexing

Classify as `unknown` when:

- there is no real SERP evidence
- top-page headings were not inspected
- the only evidence is keyword volume, a tool snapshot, or one competitor page

## Action Branches

For `parent`:

- build or strengthen a representative pillar or broad guide
- add body links from related child articles into the parent URL
- make category or hub copy visibly support the parent topic
- include the child anxieties that winners contain, but keep the opening broad enough
- avoid title-only edits as the first move when the URL is outside the candidate set
- decide which child variants deserve separate pages and link them clearly

For `child`:

- write a focused page that answers the exact user moment quickly
- keep the title and opening close to the modifier
- do not broaden so much that the exact child intent weakens
- link up to the parent hub and sideways to related child pages
- avoid forcing a child page to rank for the parent query unless GSC/SERP evidence supports it

For `mixed`:

- pick a temporary role and write it down: broad child, temporary pillar, split later, or retarget
- watch GSC for parent-query exposure and child-query drift
- strengthen internal links before making large title/body changes
- consider splitting only after enough impressions show which interpretation Google is testing

For `unknown`:

- stop title and body decisions
- gather real SERP top 10, rank ladder, lower-page and 20-30 fallen-page comparison, and, when available, GSC query spread
- mark any current conclusion as provisional

## Required Research Note Shape

Every SERP research note should include:

```md
## Parent / Child Topic Judgment

- Classification: parent / child / mixed / unknown
- Confidence: high / medium / low
- Evidence:
  - SERP breadth:
  - Rank ladder:
  - Lower-page comparison:
  - SERP features:
  - Query variants inside top pages:
  - Query variants needing separate pages:
  - GSC query spread if published:
- Decision branch:
  - <parent / child / mixed / unknown action>
```

# SEO Article Checks

Use these checks as the human-readable contract for the `article_ci.py` CLI.

## Research CI

Purpose: confirm that the article is based on source-labelled SERP evidence, starting with the project's approved keyword source, not assumed SEO common sense.

Required evidence:

- target query
- search volume or difficulty when selecting a new candidate
- date and query source
- SERP snapshot details: source, feature, reference/export, exact query, retrieval/data times, engine/settings and rank range. Google q/start and screen context are required only for actual-browser evidence.
- SERP module exclusion notes: ads, AI Overview, PAA, featured snippets, video/image packs, sitelinks, same-URL fragments, and anything deliberately not counted as organic rank
- organic top 10 all ranks, or a concrete per-rank reason when a rank cannot be inspected
- for each inspected page: title, H1, key H2/H3, page type, immediate answer, CTA or conversion path, why it is winning
- top 5 deep inspection: title, H1, H2/H3 order, immediate-answer placement, CTA/conversion path, trust display, examples, tables, question blocks when present, PAA, media/gallery use
- rank ladder analysis from 10 -> 1: what changes as pages climb, especially top 10 vs top 5 vs top 3 vs rank 1
- page type mix: whether winners are articles, LPs, category/list pages, Q&A, official/company pages, videos, or other page types
- title top 10 comparison: compare all inspected top-10 titles by subject, front-loaded words, condition words, anxiety words, solution words, naturalness, and intent fit before deciding the article title
- structure top 10 comparison: compare H1/H2/H3 order, immediate-answer placement, must-have sections, examples, tables, question blocks when present, PAA, media, and CTA paths before deciding the outline
- winning structure decision: state the final H2/H3 order, depth, intro answer, internal-link outs, and service/consultation CTA placement derived from the top-10 comparison
- top-10-to-structure rationale: how the observed top 10 pages became the planned H2/H3 structure, including what was included, excluded, split into another article, or kept intentionally thin
- lower-page comparison around ranks 11 -> 20 when visible: why similar pages may be lower, not only why winners win
- fallen-page comparison around ranks 20 -> 30: why pages similar to the planned article are outside the top 10 and what not to copy
- AI Overview, featured snippet, PAA, video, image, and ads when visible
- parent-topic or child-topic classification with evidence, confidence, and action branch
- intent-fit comparison between SERP standard answer and planned/current article
- decision: write, rewrite existing URL, split, merge, retarget, or defer

Typical status:

- `PASS`: target query, source-labelled SERP snapshot and applicable metadata, module exclusion notes, all top 10 evidence, top 5 deep inspection, ladder analysis, page type mix, title/structure comparisons, winning structure decision, structure rationale, available lower-page comparisons, feature observation status, and decision are present
- `WARN`: partial top-page evidence, missing snapshot metadata, missing module exclusion notes, missing top 5 depth, missing ladder analysis, missing page type mix, missing title/structure top 10 comparison, missing winning structure decision, missing top-10-to-structure rationale, missing around-20 or 20-30 comparison, or missing topic classification
- `NEEDS_EVIDENCE`: no SERP/GSC evidence file

Rank ladder minimum:

- `10 -> 6`: identify pages that are relevant but weaker, narrower, older, thinner, less actionable, or less trusted
- `5 -> 3`: identify what higher pages add: clearer immediate answer, stronger examples, better topical coverage, stronger author/organization trust, better internal navigation, or better SERP-format match
- `2 -> 1`: state why the top result appears to be the representative answer, not merely another good article
- Do not explain every rank by domain authority alone unless there is visible evidence. Prefer observable differences in intent fit, page type, title, structure, freshness, trust display, media, examples, CTA, and cluster support.

Top-10-to-structure rationale minimum:

- Do not move from SERP capture to article writing. First compare title patterns and structure patterns across the top 10, then decide what article structure can win.
- Map the top 10 observations to article structure, not just to a broad conclusion.
- For each major H2/H3 decision, record:
  - SERP evidence: which ranks/pages or common top-10 pattern created the need
  - Article section: the H2/H3 that will answer it
  - Decision: include, exclude, keep thin, split to child/sibling, or internal-link out
  - Reason: why this depth fits the target query and avoids intent drift
- This is the place to answer "after checking the top 10, why this outline?" A research file can have a strong rank ladder and still fail this if the final structure is not justified.

Title top 10 comparison minimum:

- Compare each top-10 title, not only the top 3.
- Record the subject, front-loaded words, condition words, anxiety words, solution words, naturalness, and intent fit.
- Explain what rank 1-3 titles do better than rank 6-10 titles.
- State which words the article title will adopt and which words it will avoid.

Structure top 10 comparison minimum:

- Compare H1/H2/H3 order across the top 10, not only a single winner.
- Record immediate-answer placement, common must-have sections, examples, tables, question blocks when present, PAA, media/gallery use, and CTA/conversion paths.
- Separate common must-have sections from differentiators.
- State which sections are deep, thin, split to another article, or linked out.

Around-20 lower-page comparison:

- Inspect visible results down to around rank 20 when feasible.
- Prioritize pages that look similar to the planned/current article.
- Record why they may be lower: child-topic drift, generic title, delayed answer, missing must-have sections, weak examples, weak trust display, no cluster support, poor freshness, or page type mismatch.
- Use the lower-page comparison to avoid copying pages that are merely indexed but not selected as the representative answer.

Fallen-page comparison 20-30:

- Inspect results around ranks 20-30 when feasible, not only page 2.
- Prioritize pages that look similar to the planned/current article, because these show what Google is not selecting for the top 10.
- Record the concrete fall reason for each useful sample: too generic, too narrow, weak answer-first structure, weak examples, outdated year, over-focus on a child query, missing comparison table, weak trust display, weak internal navigation, or page type mismatch.
- Use this section to prevent "copying a page that ranks, but not a page that wins."

Parent/child topic classification minimum:

- Use one label: `parent`, `child`, `mixed`, or `unknown`.
- Record confidence: high, medium, or low.
- Judge from SERP breadth, rank ladder, lower-page and 20-30 fallen-page comparison, page titles/H1, H2/H3 coverage, SERP features, query variants, GSC query spread when published, and existing cluster role.
- Do not judge from search volume alone. A 1000-volume query can still be a parent topic if top pages are representative guides.
- Tie the label to an action branch:
  - `parent`: pillar/broad guide, child-anxiety coverage, internal links, category or hub support.
  - `child`: exact-intent article, narrow title/opening, link up to parent.
  - `mixed`: provisional role, observe GSC, strengthen links, split or retarget only after evidence.
  - `unknown`: stop drafting and collect evidence.

## Draft CI

Purpose: confirm that title, H1, opening, structure, optional question blocks, and internal links all point at the same search intent.

Required checks:

- title reads like natural language, not a raw keyword list
- title keeps the target query's core terms semantically visible
- title length is intentional, not accidentally too vague or too long for the SERP
- title/H1/lead answer the same user moment
- lead gives an immediate practical answer before background explanation
- H2/H3 cover the SERP common must-have sections
- User anxieties and PAA questions are answered where they belong in the main structure; a separate FAQ section is optional
- internal links support the article's role in a cluster
- images/tables are planned where the article would otherwise become hard to scan
- YMYL content avoids unsafe home treatment, diagnostic certainty, and false reassurance

Typical status:

- `PASS`: structure and safety are aligned
- `WARN`: unanswered user concern, weak internal links, thin H2/H3, or unnatural title
- `FAIL`: unsafe medical/legal/financial guidance or missing article input

## Package / WP CI

Purpose: confirm that the CMS-ready artifact and live output preserve the article's intended SEO and trust signals.

Required checks:

- package shape: full HTML, body-only WordPress HTML, markdown package notes, or unclear operations note
- meta title and H1 are present and intentionally aligned
- meta description exists and answers the searcher's next step
- slug, canonical, category, author, and modified date are part of the checklist
- schema ownership is clear and not contradicted by plugin output
- embeds, images, tables, and internal links survive package conversion
- live HTML has been checked after WordPress reflection when production was touched
- markdown package notes cannot prove meta description, canonical, CMS metadata, or schema output by keyword mention alone

Typical status:

- `PASS`: metadata and package essentials are present
- `WARN`: schema/canonical/live parity not evidenced
- `NEEDS_EVIDENCE`: package or live HTML was not inspected

## Post-Publish Observation CI

Purpose: diagnose visibility without pretending Google gives a full debugger.

Required checks:

- GSC page/query data for the target URL
- exact target query exposure and child-query exposure
- query spread: whether the page is being understood as parent topic, child topic, unrelated topic, or barely understood
- live SERP snapshot for important ranking questions
- classification of the current bottleneck
- dated 7/14/28-day observation plan or actual observations
- next action: title/body rewrite, internal links, hub/category, schema/live parity, query retarget, or wait

Bottleneck vocabulary:

- `候補集合外`: Google is not showing the URL for the target query at all
- `子KW認識`: the URL appears for child queries but not the parent topic
- `titleズレ`: title/snippet does not match the query's standard answer
- `構造不足`: common must-have sections are missing or buried
- `内部リンク不足`: cluster support or anchor text is weak
- `信頼表示不足`: author, reviewer, organization, or evidence is not visible enough
- `SERP強度`: competitors, AIO, PAA, image/video packs, or domain strength make the query harder than its volume suggests
- `時間要因`: indexing is complete but reassessment may not have happened yet

Typical status:

- `PASS`: data, classification, and next action are present
- `WARN`: classification exists but observation cadence or next action is weak
- `NEEDS_EVIDENCE`: no GSC/live SERP evidence

## Human Review Rule

The CLI can only inspect text patterns. A human or agent still needs to review:

- whether the SERP standard answer was interpreted correctly
- whether the article's title is genuinely natural
- whether the medical or professional advice is appropriate
- whether the next action is proportionate to the evidence

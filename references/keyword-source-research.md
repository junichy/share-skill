# Approved keyword-source research

Start keyword and SERP research in the project's approved source when one is
specified. Otherwise choose an accessible source for the requested claim and
label it. A live search page, keyword tool, saved export, and GSC answer
different questions; do not present one as another.
This reference owns source selection for the editorial workflow and its gates.
Keep top-10 comparisons, top-5 page inspection, and query ownership checks.

## Access and budget

Inspect the available keyword-source connection and current plan before fetching. Use an
existing authorized MCP/API connection when available and its documented tools;
otherwise use the approved source's browser UI or an existing dated export. Do not invent tool
names, install a connection, upgrade a plan, or purchase credits implicitly.
MCP/API and Web can consume different credits: check the current allowance and
cost before a batch. Reuse valid exports for the same query/settings; request
only the missing data. Record unavailable features and continue independent work.
If the approved source cannot supply essential evidence, state the gap before using an
explicitly labelled alternative.

## Feature routing

Use the applicable rows, not every feature for every article. Record features
used, artifacts, and material unavailable/skipped items in the existing research.

| Research need | Keyword-source features | Use the output for |
| --- | --- | --- |
| Concrete query / SERP | 見出し抽出 first; 検索順位チェック when fresh rank evidence is needed | Ranked URLs, titles and heading comparison; open competitor pages for body evidence |
| Intent branches / topic planning | 潜在的なキーワード・質問（LSI/PAA）, サジェスト, 関連キーワード, よくある質問 | Exact query tree, reader questions, parent/child and question-block candidates |
| Same-intent coverage / ownership | 同時ランクインキーワード plus ranked URL overlap | Queries one page may own; validate against existing URLs before splitting articles |
| Demand annotation | 一括キーワード調査 | Volume and difficulty for already discovered candidates, not volume-only article selection |
| Existing article / competitor gap | 獲得キーワード調査, 獲得ページ調査, 集客コンテンツ検索 | Missing query coverage and comparable landing pages; combine with actual GSC page/query data |
| Competitor discovery / site strategy | 競合抽出, サイト検索, 一括サイト調査 | Relevant competitors and site-level patterns; reuse across articles in the same cluster |
| Missing concepts | 共起語 | Check entities, attributes and explanation gaps; never enforce keyword density or insert every word |
| Seasonality / emerging or unfamiliar topic | Googleトレンド, ニュース, Q&A, 類語・同義語, 周辺語・連想語 where available | Timing, reader vocabulary and hypotheses; verify factual claims at primary sources |
| Optional ideation | Keyword/title/heading AI suggestions | Label as generated hypotheses; never treat them as observed demand or replace the approved Codex writing workflow |

For a fixed article query, start with the source's ranked result and heading
features, then fetch the relevant intent branches and same-intent queries. For an open topic plan, start with LSI/PAA and
suggestions, then check the SERPs of shortlisted queries. On a rewrite, retain
GSC as the actual performance baseline; keyword-source estimates do not replace it.

## Evidence and stopping rules

- Save exact query, search source, feature, retrieval time, source data time
  if supplied, result URL/request ID/export path, engine, country/language/device
  when known, and covered rank range. Missing settings are `unknown`, not guessed.
- Source rank is its returned SERP snapshot, not the user's live Google screen.
  Different queries, dates, devices and sources must not be merged into one rank
  list. Preserve source attribution on any supplemental rows.
- Save top-10 title/H1/H2/H3 evidence; fetch missing page details directly and
  inspect at least the top five bodies for immediate answers, CTA, trust and
  examples. Heading extraction does not prove body content, images or quality.
- Do not invent ranks beyond a source's stated coverage or fetch Google merely
  to fill a template. Use an available deeper rank
  result when the comparison matters; otherwise record the coverage limit and a
  reasoned WARN. Essential missing top-10/intent evidence still blocks drafting.
- Google UI observation is conditional: use [serp-browser-evidence.md](serp-browser-evidence.md)
  for an actual-screen claim, AI Overview/local pack/ads/featured-result layout,
  or a material ranking discrepancy. It is not a routine second full SERP pass.
  Keyword-source PAA data remains source data. Unobserved SERP features are `not observed`,
  never `absent`. UI failure blocks only claims that depend on that UI evidence.
- Volume, traffic and difficulty are estimates/planning signals. Missing data is
  `unknown`, not zero. Rank differences and co-occurrence do not prove causation.

## Source availability

Check a provider's current features, quotas, and API schema before relying on
them. Do not claim an account or connection was verified from this reference.

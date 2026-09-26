---
name: blog-agent
description: Create or improve blog articles, research search intent and keyword relationships, diagnose SEO performance, and hand off through the project's publishing workflow.
---

# Blog Agent

Use this skill for article work. Start from the requested deliverable and the
project's current editorial rules, research, and source-of-truth documents.
Do not restart the complete production workflow for every article edit.

## Select the work

| Request | Read or do |
|---|---|
| Recurring existing-article improvement, due-date effect reviews, or daily SEO reports | Use the project's schedule and publication records. For each article, apply the relevant research, writing, and verification steps here; do not assume a separate orchestration skill exists. |
| Any reader-facing Japanese change to a title, summary, heading, paragraph, caption, CTA, or excerpt, including one sentence | Read the affected article and relevant project rules, then use [codex-writing.md](references/codex-writing.md). An exact typo, date, URL, identifier, or other mechanical value change may stay local when it requires no prose choice. |
| New article, substantive rewrite, changed query/intent/outline, or article SEO strategy | Read [editorial-workflow.md](references/editorial-workflow.md), its selected stage references, and [codex-writing.md](references/codex-writing.md). Preserve research and structure gates, then use the conversational writing workflow for substantive prose. |
| Keyword discovery or a topic tree | Read [lsi-paa-keyword-discovery.md](references/lsi-paa-keyword-discovery.md). |
| Sequence multiple related articles | Read [bottom-up-article-sequencing.md](references/bottom-up-article-sequencing.md). |
| Decide which article owns nearby queries | Read [serp-ownership-check.md](references/serp-ownership-check.md). |
| GSC-backed article selection, search performance comparison, query/page visibility, or indexing diagnosis | Use [GSC evidence](references/gsc-evidence.md); reuse valid project evidence. |
| Diagnose an existing article's weak visibility or ranking | Read [rewrite-diagnosis.md](references/rewrite-diagnosis.md); collect evidence for the suspected cause before changing copy. |
| Run an article/structure inspection report | Read the relevant [checks.md](references/seo-checks/checks.md), [structure-gate-checks.md](references/seo-checks/structure-gate-checks.md), or [diagnosis-template.md](references/seo-checks/diagnosis-template.md). |
| Save, update a ledger/KPI, or prepare a WordPress draft | Follow the project's existing instructions and profile; do not restart article research. |
| Google technical SEO or official guidance only | Use current Google documentation; [search-central-index.md](references/seo-checks/search-central-index.md) is the local routing index. |

A title rewrite that changes the promised answer, audience, or target query is
substantive work. A wording-only edit does not require a new top-ten comparison
when those decisions remain unchanged. Reuse relevant, still-current research;
refresh it when the requested conclusion depends on present search results.

## Evidence and editorial ownership

- Codex owns research, SERP-based structure, factual verification, article
  assembly and proofreading. For substantive prose, follow
  [codex-writing.md](references/codex-writing.md). An external writing model
  may be used only when the project explicitly authorizes it. Image generation
  follows the project's existing provider rules.
- Use [Japanese writing review](references/japanese-writing.md) for Japanese drafting and editing. Verify
  source-dependent facts, preserve the writer's voice, and correct concrete
  defects within the authorized article scope before saving the completed draft.
- Preserve a user-designated final manuscript verbatim unless edits are requested,
  including previously saved Gemini text. Historical drafts, billing records and
  unresolved reservations remain intact; changing writers does not resolve them.

- Start keyword and SERP research with the project's approved keyword source.
  Read [keyword-source-research.md](references/keyword-source-research.md) for feature selection,
  access, cost and source-labelled evidence. Use Google in Chrome only when
  actual-screen evidence is needed, following [serp-browser-evidence.md](references/serp-browser-evidence.md).
- Keep organic ranks separate from ads and SERP features. Do not infer observed
  rank from a web-search summary, or treat a plausible ranking explanation as
  demonstrated causation.
- Keep the article's title, opening, headings, examples, and any optional
  question block on the same search intent. A FAQ section is not a required SEO
  element and must not be added by default. Answer a question in the section
  where it naturally belongs, and add a short question block only when it
  resolves a distinct reader concern or the user explicitly requests it.
  Never add repeated questions for rich-result eligibility. Preserve exact
  query spelling and distinguish an observed zero from missing keyword-volume
  data.
- Prefer LSI/PAA/topic-tree evidence for query relationships; bulk volume is
  supporting information. Avoid duplicate authoritative articles for the same
  intent without checking ownership and overlap.
- Preserve facts, sources, certainty, the writer's voice, and project-specific
  requirements. Do not add unsupported experience or sales claims for style.
- Fix only the requested boundary. Finding an unrelated SEO weakness does not
  authorize rewriting the article, publishing it, or changing its ledger.

## Stage-specific references

Read only the reference needed for the active stage:

- [serp-intent-gates.md](references/serp-intent-gates.md): full article research,
  intent, title, and structure evidence.
- [title-structure-rules.md](references/title-structure-rules.md): title and
  heading conventions when those elements change.
- [regional-winning-structure.md](references/regional-winning-structure.md):
  local/regional comparison and service content.
- [article-production.md](references/article-production.md): body writing and
  article package requirements.

## Verification and handoff

Run the applicable content, structure, factual and rendering checks on the
Codex draft, correcting defects within the requested scope. Check storage
readback after saving; a saved draft is not publication or user acceptance.
Do not manufacture research artifacts or claim unrun checks passed.

Report the delivered article or change, its saved location when applicable,
checks actually run, and missing evidence that affects the result. Saving,
external ledger updates, scheduling, and publication follow the user's existing
authorization and the project's current workflow. This skill grants none of
those actions by itself and does not require a new approval for an already
authorized action within the same scope.

# SEO Debug Patterns

Use these patterns when an indexed article does not rank as expected. Classify before changing title, body, images, or schema.

## Candidate Set Problems

`候補集合外`
- Symptom: indexed URL has no impressions for the exact target query.
- Look for: no GSC exact-query row, no live SERP appearance, weak internal links, unclear title/topic, wrong representative URL.
- First moves: strengthen cluster links and hub, make title/opening/H2 more representative of the parent topic, verify canonical/live metadata.

`子KW認識`
- Symptom: page gets impressions for child queries but not the parent query.
- Look for: child-query rows in GSC, title or H2 biased to symptoms/examples, missing broad overview sections.
- First moves: broaden the page toward the parent intent or intentionally retarget as a child page.

`代表URLズレ`
- Symptom: Google prefers another page on the same site or an old URL.
- Look for: site: search, canonical mismatch, internal links pointing to multiple similar URLs, redirects, category pages.
- First moves: consolidate links, add redirects/canonical clarity, update hub links.

## SERP Fit Problems

`titleズレ`
- Symptom: page is indexed but impressions are low or snippet does not match the target moment.
- Look for: title uses editor-side wording, late action word, unnatural separators, missing condition/anxiety/action terms.
- First moves: rewrite title and H1 around the user's immediate action.

`冒頭即答不足`
- Symptom: article has relevant sections but feels slow or explanatory.
- Look for: background before answer, no first-step instruction, delayed triage.
- First moves: put the standard answer and next action in the first paragraph.

`構造不足`
- Symptom: article covers the topic but does not match the SERP's answer shape.
- Look for: missing must-have H2/H3, no examples, no decision branches, or unanswered PAA/user concerns. A missing FAQ section is not a defect by itself.
- First moves: add the missing answer modules before adding differentiation.

`ページタイプ不一致`
- Symptom: our page is a blog note while winners are calculators, directories, service pages, videos, UGC, or official docs.
- Look for: SERP feature mix and top 10 page types.
- First moves: change article format, add the missing media/template/table, or choose another query.

## Trust And Cluster Problems

`信頼表示不足`
- Symptom: article content is strong but competitors show clearer author/reviewer/organization proof.
- Look for: author mismatch, reviewer missing, schema conflicts, weak first-screen trust signals.
- First moves: improve visible trust layer and schema/plugin parity.

`内部リンク不足`
- Symptom: article is isolated or only linked from weak pages.
- Look for: few inlinks from cluster articles, weak anchors, category hub does not explain the topic.
- First moves: add body links from relevant cluster pages, improve category/hub copy, use anchors matching the parent topic.

`SERP強度`
- Symptom: volume looks manageable but top 10 is held by high-trust brands, AIO sources, rich media, or entrenched pages.
- Look for: AIO, PAA, video/image packs, strong brand pages, fresh UGC, top pages with extensive clusters.
- First moves: decide whether to build a pillar/hub and observe longer, or retarget to a smaller child query.

`動画/画像接続不足`
- Symptom: video or image packs appear, but owned or supporting media does not appear or is not connected to the article.
- Look for: video pack sources, image pack themes, embeds, timestamps, schema, transcript/supporting text, media filenames/alt text.
- First moves: add purposeful embeds, connect the article to the media's exact answer, and avoid using video as a substitute for the SERP standard answer.

`CMS/liveメタデータズレ`
- Symptom: local article/package looks correct, but live HTML or SEO plugin output still shows old title, author, schema, date, or description.
- Look for: live `<title>`, meta description, canonical, schema JSON-LD, author, dateModified, plugin tables/options, rich-result inspection.
- First moves: fix the live source of truth, not only the markdown/package. Recheck the public URL after reflection.

`時間要因`
- Symptom: live and indexed page is corrected, but reassessment has not happened yet.
- Look for: very recent modified date, few crawl cycles, early impressions only.
- First moves: request indexing if appropriate, add internal links, observe 7/14/28 days before more large edits.

## Default Fix Order For Parent-Topic Failure

When a page is indexed but not entering the parent query's candidate set, do not start with title-only edits unless the title is clearly wrong.

Preferred order:

1. Confirm live title/H1/meta/schema/canonical/dateModified.
2. Add or strengthen internal body links from the existing topical cluster.
3. Improve the category or hub page so the cluster has a visible parent.
4. Rework the article opening and H2/H3 toward the parent SERP standard answer.
5. Adjust title only after the representative-topic problem is understood.
6. Observe GSC query spread at 7/14/28 days.

Title-only edits are useful when `titleズレ` is the main bottleneck. They are usually insufficient for `候補集合外`, `子KW認識`, or `内部リンク不足`.

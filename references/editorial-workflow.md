# Full editorial workflow

Read this reference for a new article, a change to search intent or article
structure, a substantive rewrite, or an SEO diagnosis that needs this evidence.
It is not required for a bounded wording correction that preserves the approved
query, intent, facts, and structure. Use relevant existing research when still
current; refresh the observations needed for the present claim.

Follow only the stages needed for the requested deliverable. Article research
and production retain the evidence gates below; an operations-only task follows
the project's existing instructions without restarting research. Script paths
are relative to the blog-agent skill root, and artifacts belong to the project.

## Operating model

調査の入口と取得元は [keyword-source-research.md](keyword-source-research.md) に従う。承認済みのキーワードソースの見出し抽出・関連機能から始め、Google実画面は必要な場合だけ確認する。

順番は固定します。

1. SEO design and SERP intent diagnosis: this skill, with live Google docs checked directly when official guidance or technical SEO confirmation is needed
2. Keyword discovery and topic architecture: use LSI/PAA/tree-first discovery with [references/lsi-paa-keyword-discovery.md](lsi-paa-keyword-discovery.md)
3. Bottom-up article sequencing before writing multiple related articles: use the LSI/PAA planning tree, source strength, intent width, action closeness, and duplication risk with [references/bottom-up-article-sequencing.md](bottom-up-article-sequencing.md)
4. Mandatory article evidence check before title, outline, writing, publish, or diagnosis decisions for concrete queries: this skill, with `scripts/article_ci.py` when a local research/package artifact exists
5. Structure check before final outline or writing when H2/H3, contextual internal links, CTA placement, summary links, trust/site identity, or benchmark-inspired architecture matters: this skill, with `scripts/seo_article_structure_gate.py` when a local artifact exists
6. Production and writing: this skill, only after research and structure decisions have been written
7. Operations handoff: follow the current project profile / repo instructions
8. Project profile / repo instructions: site-specific overrides

Core rules:

- 具体 query やテーマがある場合、SERP 観察を飛ばさない
- キーワード探索は一括キーワード調査ではなく、LSI/PAA/ツリーを起点にする。bulk volume は既知候補への注釈や表記ゆれ発見に使い、島・親子・記事順の主材料にしない
- LSI/PAA/ツリーでは、query、tree path、source surface、volume、意図分岐、site fit、記事役割を保存する。クラスタ名より、検索者の不安・比較・条件・次行動の枝を優先する
- 外部ツールで取った query は exact に扱う。表記ゆれやスペース有無は勝手に統合せず、`0` は既知のゼロ、`unknown` は未取得として扱う
- 必要な探索ルールはこの skill の references に集約する
- 複数記事をボトムアップで作る場合は、volume順ではなく `狭い意図` `入ってくる線` `行動の近さ` `SERP独立性` `重複リスク` `あとで束ねやすいか` で順番を決める。大きな親記事は最初から完成させず、子記事の反応を見て後から束ねる
- 同じ島で親queryの入口ページが必要な場合は、`親記事を書く -> 子記事を書く -> 親記事へ戻り整合性や専門性をチェック` を基本形にする。ただし最初の親記事は完成版の大全ではなく、検索入口・判断ハブ・子記事への分岐表として薄く作り、子記事公開後に内部リンク、分岐文言、専門性、受診/相談導線を再調整する。
- 記事ごとに `深く書く` `短く触れる` `書かない` を決め、所有queryが重なる記事を同時に作らない
- 計画ツリーの順番をそのまま執筆順として扱わない。記事制作へ入る直前に、同じ島の近接queryと既存台帳URLを見て `SERP所有権確認` を行う。特に不安系、時期系、探し方系のように重複しやすい島では、最初の着手は記事本文ではなく「どの記事がどのqueryを所有するか」の確認にする
- 記事の作成済み判定はquery行単位で行う。同じ島、slug、ownerSlugの親記事を作っても、兄弟・深掘り・言及queryを作成済みにはしない。本文で明示的に扱ったqueryだけをcoverage mapに列挙し、その行だけを状態更新する。たとえば `長寿祝い一覧表` を作っても、`100歳は 何 寿` は別途扱うまで未作成のままにする
- 地域系query（`<service> 地域`, `<service> 地域 おすすめ`, `<service> 地域 料金`, `<service> 地域 比較` など）では、本文作成前に [references/regional-winning-structure.md](regional-winning-structure.md) を読む。地域分類を主題にせず、実際に上位に出る地域まとめ/比較ページの構造に合わせて、早い比較表、実店舗/施設カード、料金/総額、含まれるもの、公式/detail導線、必要な補足質問を設計する
- SERP は承認済みのキーワードソースの見出し抽出を起点に取得する。取得元・機能・日時・参照先・条件・順位範囲を research に残す。その順位をユーザーのGoogle実画面の順位とは呼ばない
- Google実画面が必要な場合だけ [SERP browser evidence](serp-browser-evidence.md) に従い、`q` / `start`、取得時刻、location / personalization、SERP featuresを別記する。取得元や日時の違う順位を混ぜない
- 広告、AI Overview、PAA、強調スニペット、動画/画像パック、サイトリンク、同一URLフラグメントは organic rank と混ぜない。除外した SERP module と同一URLフラグメントの扱いを research に残す
- 必要な SERP を観察できない場合は、具体的な権限・接続・CAPTCHA・通信の問題を記録する。旧スキル名がないことだけを停止理由にせず、現在の操作APIを確認する。観察できなかった順位や検索意図を推測で確定しない
- 具体 query の新規記事・改修では、title / 構成 / リライト方針を確定する前に、自然検索上位10件すべての `rank` `URL` `title` `H1` `主要H2/H3` `page type` `冒頭の即答` `CTA/導線` `勝っている理由` を research に保存する
- 上位5件は URL 列挙で終わらせず、title / H1 / 主要 H2-H3 / 即答位置 / CTA / 信頼表示 / 例・表・画像 / 任意の質問ブロックまで深く見る
- SERP を見た後、すぐ本文・WP下書き・package 作成へ進まない。Research CI 相当の分析を通し、`PASS` または理由付き `WARN` になるまで title / outline / article を確定しない。`NEEDS_EVIDENCE` は停止条件にする
- title を出す前に、自然検索上位10件の `Title Top 10 Comparison` を作る。各 title の主語、前半語、条件語、不安語、解決語、自然さ、検索意図との距離を比較し、なぜ自記事の title が勝ち筋に乗るのかを書く
- 構成を出す前に、自然検索上位10件の `Structure Top 10 Comparison` を作る。各ページの H1/H2/H3 の順番、即答位置、必須セクション、例・表・質問ブロック・画像/ギャラリー・CTA を比較し、共通必須要素と捨てる要素を分ける。FAQ見出しは必須要素にしない
- 構成を作る時は、H2だけの平板な目次で逃げない。各H2について、本文に入る前に `このH2を支えるH3候補`、`H3に分ける判断軸`、`H3を作らない理由` のいずれかを明記する。理由なしにH2直下へ長い本文を置く構成は `Structure incomplete` として止める
- H3は飾りではなく、検索意図の分岐、手順、判断軸、原因分類、比較条件、注意点、例外、読者の次の行動を分けるために使う。1つのH2で複数の問い・条件・手順を扱うなら、H3へ分解する
- H3を作らないH2は、短い即答、導入、まとめ、任意の質問ブロック導入、または単一メッセージのCTAに限る。目安としてH2本文が3段落を超える、表の前後に説明が必要、列挙が3項目以上ある、内部リンクへ分岐する、具体例が複数ある場合はH3化を再検討する
- `Winning Structure Decision` として、上位10件の比較から導いた最終 H2/H3、各セクションの深さ、内部リンクへ逃がす項目、サービスページや相談導線へ渡す位置を明記してから本文に入る。H2だけの構成にする場合は、SERP上位も同様にH2中心で勝っている証拠と、自記事でH3を使わない理由を残す
- H2/H3、内部リンク、CTA、まとめリンク、信頼表示が重要な記事では、本文に入る前に構造チェック結果を research / package に残す。`FAIL` のまま本文・WP下書き・公開へ進まない
- 上位10件の rank が欠ける場合は、欠けた rank ごとに `blocked` `not fetched` `SERP feature only` `duplicate fragment` `JS required` など具体理由を残す。理由なしの top 8 / top 9 で title や構成を確定しない
- 上位10件は横並びで終わらせず、10位から1位へ登るほど何が変わるのか、なぜその順位になっているのかを `rank ladder` として書く
- 構成を作る前に、上位10件からどの H2/H3 を採用し、どれを捨て、どれを内部リンク先へ逃がすかを `Top 10 -> Article Structure Rationale` として書く
- 11〜20位と、取得可能なら20〜30位前後の類似ページを比較する。承認済みソースの取得範囲外は推測せず、`fallen-page comparison 20-30` に範囲制限と理由付きWARNを記録する。テンプレートの穴埋めだけを理由にGoogle検索へ進まない
- 記事の現在地を機械的に確認したい場合は、`scripts/article_ci.py` で `PASS / WARN / FAIL / NEEDS_EVIDENCE` のレポートを作る
- 既存記事や公開済み記事では、順位だけで判断しない。GSC で target query / variant query が対象 page に表示されているかを `target-query visibility` として確認する。表示されていない場合は title 微修正ではなく、query-page fit / cluster / internal link / entity 認識の診断を優先する
- 検索ボリューム、競合性、SEO難易度などの外部指標は planning signal として扱う。順位不振の直接原因として断定しない。ranking proof は実 SERP と GSC の query/page evidence で見る
- 「良い記事なのに弱い」場合は、本文を直す前に barrier を分類する: index/crawl、intent/page type mismatch、target-query visibility 不足、authority/time、semantic depth 不足、entity/brand recognition 不足、差別化不足、cluster/internal link 不足
- AI Overview / AI Mode / 生成AI検索を意識する場合も、AI専用の小手先施策から始めない。crawlable HTML、明確な見出し、早い即答、自己完結した説明ブロック、表/図解、内部リンク、entity の一貫性を優先する
- FAQ見出しやFAQPage構造化データは必須にしない。検索者の疑問はまず該当するH2/H3の本文で回答し、本文の流れに入らない独立した不安が残る場合だけ、短い質問ブロックを置く。リッチリザルト獲得を目的に質問を増やさない
- 図解、比較表、カスタム画像は rescue ではなく amplification として使う。検索需要がある、GSC impressions がある、または比較/手順/時期/判断軸が複雑な記事で優先する。intent ズレや target-query visibility 不足を画像だけで解決しようとしない
- ブランドやサイト entity が効く領域では、site/category/audience/distinct point を記事内外で一貫させる。Who/what is this site?、誰向けか、どの地域/領域で強いかが曖昧なまま本文だけ増やさない
- 公開後に直す前提で進めない。作る前に `SERP 上位ページと予定記事の主題比較` を行う
- 低ボリューム query ほど、検索意図の芯から少しでもズレると負ける前提で進める
- 低ボリュームの子 query を見つけてもすぐ専用記事化しない。SERP が親記事型なら、まず親記事の一部として回収する
- 親記事は topic map と判断基準を担い、子記事は 1 つの具体不安・条件・行動を深掘りする。同じ定義、比較表、一般論を両方で厚く書かない
- 親子・兄弟 query の SERP が大きく重なる場合は、別記事を増やす前に `merge into parent / focused child / sibling article / retarget existing URL` の分岐を明記する
- 小手先の調整より `上位ページと予定記事の主題一致` を優先する
- `title`、導入、H2/H3、本文例文、任意の質問ブロックが同じ検索意図に向いているか最後まで確認する
- 最終アウトライン確認では、`H2-only escape check` を必ず行う。H2の半数以上がH3なし、または1つでも長文H2がH3なしの場合は、`OK / Split to H3 / Keep H2-only with reason` を各H2に付けてから本文へ進む
- どこかの段階を省略した場合は、理由を明記する


## Stage 1: SEO design

まずこの skill で search intent と SERP 上位構造を整理する。Google 公式 guidance、technical SEO、index/crawl/schema/title/snippet の確認が必要なら、[references/seo-checks/search-central-index.md](seo-checks/search-central-index.md) または live Google docs を直接確認する。

最低限固めること:

- target query / search intent
- SERP 上位10件すべての構造 evidence、欠落 rank ごとの理由、SERP module 除外メモ、同一URLフラグメントの扱い、10 -> 1 の順位差分、top 10 から構成へ落とした理由、20 -> 30 前後の落下ページ比較
- Page Type Mix: 記事、LP、カテゴリ/一覧、Q&A、動画、公式/企業ページなどの比率と、どの page type が上位で勝っているか
- Title Top 10 Comparison: 上位10件の title を横並びにし、勝ち語彙、前半語、条件語、不安語、解決語、自然さ、採用/不採用理由を比較する
- Structure Top 10 Comparison: 上位10件の H1/H2/H3、即答位置、質問ブロック/PAA、画像/表/事例、CTA/導線を横並びにし、共通必須要素と不足しがちな要素を比較する
- Winning Structure Decision: 上位10件の比較から、勝つための最終 H2/H3、深さ、順番、内部リンク・サービス導線の置き方を決める
- parent / child / sibling classification and topic split decision
- cluster writing sequence: parent-first skeleton / child articles / parent return-check when a parent query must act as the entrance
- SERP standard answer
- AI Overview / featured answer elements if present
- target-query visibility / GSC query spread if the page or related pages are already published
- semantic depth: entities, attributes, relationships, comparison axes, examples, and missing formats
- entity / brand clarity: site category, audience, distinct point, author/operator signals, and whether the page reinforces them
- 差別化余地
- 内部リンク方針
- visual / diagram opportunity: whether an eyecatch, comparison table, flow, timeline, checklist, or infographic would clarify the intent
- practical recommendation
- regional winning structure decision when the query has a region/local modifier: whether the page should be a provider roundup, local service guide, marketplace/category support page, single-provider LP support, or parent hub; include early comparison table columns, provider/store card fields, price/total-cost breakdown, and lower-area/condition link routes

キーワード探索や島設計から入る場合は、[references/lsi-paa-keyword-discovery.md](lsi-paa-keyword-discovery.md) を読む。LSI/PAA/ツリーで検索者の思考の枝を取り、bulk volume は補助情報として後から付ける。

同じ島から複数記事を書く場合、本文作成前に [references/bottom-up-article-sequencing.md](bottom-up-article-sequencing.md) を読み、各記事の `deep / mention / exclude` を決める。

計画ツリーから記事制作へ進む時は、最初に着手する島について [references/serp-ownership-check.md](serp-ownership-check.md) の `SERP所有権確認` を行う。既存台帳のslug/liveURL、近接query、重複リスク、SERP overlapを見て、新規記事、既存リライト、追記、言及、保留を決め、researchに保存し、必要なら計画ツリーにも判断を戻してから本文に入る。

具体 query の記事制作・改修では、この後に [references/serp-intent-gates.md](serp-intent-gates.md) を読む。research ファイルがある場合は、本文作成前に `scripts/article_ci.py --stage research --fail-on needs_evidence` を実行し、`NEEDS_EVIDENCE` なら不足 evidence を集め直す。

## Stage 2: Production

本文作成前に、必ず次を通す。

1. SERP answer extraction
2. Title Top 10 Comparison
3. Structure Top 10 Comparison
4. H2-only escape check: every H2 has supporting H3s or an explicit reason to stay H2-only
5. Winning Structure Decision with final H2/H3 outline and section-depth notes
6. Structure check result for H2/H3, internal links, CTA, summary links, and trust/site identity: `PASS` or written `WARN`
7. AI Overview / featured answer extraction
8. Intent-fit comparison
9. Parent / child topic classification
10. Target-query visibility / barrier diagnosis when working on an existing or published page
11. Semantic depth and entity clarity check
12. Visual / diagram opportunity decision
13. Title intent lock
14. Structure parity
15. Research CI result from `scripts/article_ci.py`: `PASS` or written `WARN`

title や構成を作る時は [references/title-structure-rules.md](title-structure-rules.md) を読む。
本文と package を作る時は [references/article-production.md](article-production.md) を読む。

`Mismatch risk`、`NEEDS_EVIDENCE`、article check `FAIL`、未完の Title / Structure Top 10 Comparison、または未完の `H2-only escape check` が残る場合は、本文を書き始めない。

## Stage 3: Operations Handoff

記事本文、package、research が揃ったら、案件の現行 repo instructions / project profile を確認する。

扱うこと:

- article 保存
- package 保存
- research 保存
- prompt 保存
- 台帳更新
- KPI 更新
- 施策ログ更新
- 必要なら画像連携
- 必要なら WordPress 下書きまたは公開反映

## Stage 4: Rewrite / post-publish diagnosis

公開後に「弱い」「順位が出ない」「思った順位にいない」と分かった場合は、細かい修正から始めない。

まず [references/rewrite-diagnosis.md](rewrite-diagnosis.md) を読み、上位ページと自記事を比較してから decision を決める。

## Handoff contract

Stage 1 -> Stage 2:

- target query / intent
- SERP observations
- target-query visibility / GSC query spread when available
- Title Top 10 Comparison
- Structure Top 10 Comparison
- H2-only escape check with per-H2 split/keep reasons
- Winning Structure Decision with final H2/H3 outline
- SERP standard answer
- AI Overview / featured answer elements if present
- intent-fit comparison
- barrier classification for existing or weak pages
- parent / child / sibling classification
- keyword discovery artifacts when used: LSI/PAA/tree source, tree path, volume source, exact-miss notes, planning tree
- topic split decision and duplication boundary
- recommended angle
- semantic depth and entity/brand clarity notes
- visual / diagram opportunity decision
- internal linking guidance
- cluster writing sequence and parent return-checklist when multiple child articles are planned

Stage 2 -> Stage 3:

- approved title
- slug
- article body
- package path or final package
- assets / prompts that need saving

# Rewrite Diagnosis

公開後に順位が弱い、想定 query に出ない、既存記事をリライトしたい時に読む。

GSCを読む際は [GSC evidence](gsc-evidence.md) に従う。
取得済みの同条件データを再利用し、GSC平均順位と実検索の順位を区別する。

## First response

細かい修正から始めない。まず上位ページと自記事を比較する。

最初にやること:

1. 実検索または GSC で、対象 query と現在順位/露出を確認する
2. GSC で target query / variant query が対象 page に表示されているかを確認する
3. その query の上位ページを再確認する
4. `上位ページ vs 自記事` の主題・title・H2/H3・冒頭・例文・必要な質問ブロック・内部リンクを比較する
5. 弱さを分類する
6. decision を research または KPI 施策ログに残す

順位、検索ボリューム、外部ツールの競合度だけで原因を決めない。外部指標は planning signal として使い、順位不振の diagnosis は SERP と GSC の query/page evidence で行う。

## Weakness classification

- index / crawl 問題
- target-query visibility 不足: そもそも対象 page が狙い query で表示されていない
- intent / page type mismatch: SERP が求めるページ型と自記事の型が違う
- 主題ズレ
- title ズレ
- 冒頭の即答不足
- 共通必須要素不足
- semantic depth 不足: entity、比較軸、条件、関係性、具体例が薄い
- 例文 / テンプレート不足
- entity / brand recognition 不足: サイトや運営主体、対象読者、地域/領域の強みが曖昧
- 内部リンク不足
- ドメイン / 被リンク / 時間要因

主題ズレや必須要素不足がある場合は、alt、細かな表現、画像だけを先に直さない。

画像や図解は、需要や impressions がある記事の理解を強めるために使う。target-query visibility がない、または intent がズレているページを画像だけで押し上げようとしない。

## Comparison table

```md
Query:
- <target query>

Current position / evidence:
- <GSC or live SERP evidence>

Target-query visibility:
- <target query and variants appear / do not appear for the target page in GSC>

SERP standard answer:
- <上位とAI Overviewが共通して返している答え>

Current article:
- <現記事の主題、title、H2/H3、冒頭、例文、必要な質問ブロック>

Top-page gap:
- <足りない主題、型、例文、構造、即答>

Barrier classification:
- <index/crawl / visibility / intent mismatch / authority-time / semantic depth / entity recognition / differentiation / cluster-link>

Visual / diagram decision:
- <必要 / 不要 / 後回し。理由: demand, impressions, comparison complexity, or intent risk>

Revised article:
- <寄せ直す主題、title、構成>

Decision:
- <既存URLを寄せる / 専用記事を作る / target query を変える / 内部リンクだけ強化して観測 / 7日-14日観測>
```

## Decision options

- 既存URLを寄せる
- 専用記事を作る
- target query を変える
- 内部リンクだけ強化して観測する
- 図解や比較表を追加して観測する
- 7日-14日だけ観測して GSC の query/page evidence を待つ

この decision を KPI 施策ログまたは research に残す。

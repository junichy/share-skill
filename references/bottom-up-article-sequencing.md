# Bottom-Up Article Sequencing

複数の関連queryから記事を書く時は、親記事から大きく作らない。LSI/PAA/tree-first の planning tree を使い、まず狭い意図で勝てる記事を作り、GSC / SERP の反応が出た束を後から親記事やハブ記事でまとめる。

ただし、親記事の設計図は先に作る。親記事を完成させるのではなく、どの子記事が何を所有するかを先に正規化する。

## Parent -> Child -> Parent Return Pattern

同じ島で親queryの検索入口が必要な場合は、単純な「低volumeから順に子記事だけを書く」でも「高volumeの親記事を全部盛りで先に完成させる」でもなく、次の順番を基本形にする。

```text
親記事を書く
  -> 子記事を書く
  -> 親記事へ戻り、整合性・内部リンク・専門性を再チェックする
```

使う条件:

- 親queryのvolumeやSERP露出が大きく、クラスタの代表URL/入口が必要
- 子queryが複数あり、それぞれ検索意図が狭く、別記事で深掘りできる
- 親記事だけで全部を書くと、子記事の `deep` を食ってカニバリしやすい
- 子記事だけ先に作ると、サイト内でクラスタの親子関係が見えにくい

最初の親記事でやること:

- 親queryの標準回答、全体像、判断軸、分岐表を作る
- 子記事候補へ内部リンクする場所を用意する
- 子記事が未公開なら、将来リンク予定の分岐文言だけ先に正規化する
- 子記事が所有する具体不安・条件・疾患・手順を厚く書きすぎない

子記事でやること:

- 1つの具体不安、条件、行動、疾患疑いを `deep` として深掘りする
- 親記事の定義や一般論は1〜2文に抑える
- 親記事へ戻るリンクと、近い兄弟記事への必要最小限のリンクを入れる
- sibling の `deep` を奪わないように `mention / exclude` を明記する

親記事へ戻る時のチェック:

- 子記事への内部リンクが、導入直後、判断表、該当H2のいずれかにあるか
- 親記事の分岐文言と子記事のtitle/H1/H2が一致しているか
- 親記事が子記事の詳細領域を厚く書きすぎていないか
- 子記事で増えた専門性や注意点が、親記事の要約/判断表に反映されているか
- CTAや相談導線が緊急度別に矛盾していないか
- GSCで親queryが子記事に流れていないか、または子queryが親記事に吸われすぎていないかを公開後に確認する

この pattern でも、本文着手前の `SERP所有権確認` は省略しない。親記事を先に書く場合でも、親記事の `deep / mention / exclude` を決めてから本文に入る。

## Normalized fields

各 query / node は、記事順を決める前にこの形へそろえる。

```md
Query:
- query:
- volume:
- sourceLabel: lsi / paa / tree_path / related_search / bulk_volume / gsc / manual
- treePath:
- branchStrength: high / medium / low
- sourceStrength: high / medium / low
- intentCategory: 不安 / 探す / 時期条件 / 成果選考 / お金 / 働き方 / 比較 / 定義 / その他
- intentWidth: narrow / medium / broad
- actionCloseness: high / medium / low
- serpIndependence: high / medium / low / unknown
- duplicationRisk: high / medium / low
- bundleFit: high / medium / low
- articleDecision: write-now / bundle-first / merge-into-existing / hold / no-article
- ownerArticle:
- deep:
- mention:
- exclude:
- splitTrigger:
```

## Tree and source interpretation

- `treePath`: どの親/枝から出たか。島の構造と重複リスクを見る
- `branchStrength`: 同じ枝に近い query が複数あるか、意図が太いかを見る
- `sourceStrength`: LSI、PAA、tree path、GSC、bulk volume などの根拠の強さを見る
- `sourceLabel`: PAA-only、bulk-only、manual-only を記事候補として過信しないために残す

判断:

- branchStrength 高 / intent narrow: 小さく勝てる子記事候補
- branchStrength 高 / intent broad: 重要だが重複危険。束ね記事または所有範囲の明確化が必要
- treePath が親に近く sourceStrength 高: ハブっぽい。初手で大きくしすぎない
- volume 大 / sourceStrength 低: ブランド、一覧、求人、辞書的意図の可能性。SERP type確認まで保留
- volume 小 / branchStrength 高: 共通不安の可能性。volumeだけで捨てない

## Score rule

ボトムアップの優先度は volume 順にしない。

```txt
bottomUpScore =
  intentNarrowness
+ branchStrength
+ actionCloseness
+ serpIndependence
+ bundleFit
- duplicationRisk
- parentSufficiency
```

各値は `high = 2`、`medium = 1`、`low = 0` を基本にする。`unknown` は原則 `0.5` として扱い、SERP未確認の過信を避ける。

volume は tie-breaker と planning signal。`volumeが大きいから先に書く` とはしない。

## Article decision

### write-now

次を満たすもの。

- intent が狭い
- 1記事で答え切れる
- LSI/PAA/tree/GSC のいずれかで根拠がある
- 行動に近い
- SERP が親queryと独立している
- 他記事との所有範囲が切れる

### bundle-first

次を満たすもの。

- 同じ枝に複数queryが集まる
- 不安語や条件語が複数queryにまたがる
- 別記事にすると定義・一般論・比較表が重複しやすい

まず1本の束ね記事で `deep` を決め、GSCで表示queryが分かれたら分割する。

### merge-into-existing

次を満たすもの。

- SERP上位が既存記事や親記事と大きく重なる
- queryの答えが既存記事のH2/H3で十分
- 単独記事にすると同じ説明を繰り返す

### hold

次を満たすもの。

- SERP type が未確認
- 求人一覧、ランキング、ブランド指名、サービス比較など、記事で勝てるか不明
- volume はあるが LSI/PAA/tree 上の根拠が薄い

### no-article

次を満たすもの。

- 事実上の表記ゆれ
- PAAの質問だけで検索需要やSERP独立性がない
- 自サイトの目的と離れる

## Question and PAA handling

PAA由来の質問queryは、すぐ単独記事にしない。

- `？` が付く質問文、または `ですか` `ますか` `どのくらい` などの質問形で、volumeが0または未取得なら `merge-into-existing` を優先し、該当するH2/H3の本文で答える
- 同じ枝で何度も出る質問は、所有記事のH2/H3で答えられるかを先に確認する。FAQ見出しを増やす理由にはしない
- 質問形でも volume があり、SERP上位が専用記事で独立している場合だけ `write-now` 候補に戻す
- sourceStrength が低く、volume<=50 の孤立queryは、原則 `hold` か近い記事の `mention`

## Ownership rule

記事ごとに必ず `deep / mention / exclude` を決める。

```md
Article:
- target:
- role: child / sibling / bundle / hub
- deep:
  - <この記事が深く答えるquery>
- mention:
  - <短く触れて内部リンクするquery>
- exclude:
  - <書かないquery>
- internalLinks:
  - to:
  - from:
- splitTrigger:
  - <GSCで表示/CTR/順位が出たら分割する条件>
```

重複防止:

- `deep` が2記事で重なったら、片方を `mention` に落とす
- 子記事の冒頭で親の定義を厚く書かない。1〜2文だけにする
- 不安系は `やめとけ` `意味ない` `後悔` `きつい` を最初から細かく分けすぎない
- 条件系は `期間` `何ヶ月` `週何日` `いつから` `大学何年` の所有者を先に決める
- 探す系は `探し方` `サイト` `アプリ` `何社受けるべき` `応募前チェック` を同じ束として扱う

## Query coverage boundary

記事の所有範囲と、計画ツリー上のqueryを作成済みとする状態は分けて扱う。

- 同じ島、slug、ownerSlugに属することは、記事が存在することを示すだけで、各queryの本文カバレッジを証明しない
- 記事作成・公開後に状態を更新する前に、`mainQuery`ごとのcoverage mapを作る。対象は、完成本文で明示的に答えたqueryと、短く触れて内部リンクを置いたqueryに限る
- coverage mapにない兄弟・`deep`・`mention`・`hold`行は、親記事と同じslugでも未作成・計画中のまま残す
- `長寿祝い一覧表`を作成しても、本文で独立した回答をしていない`100歳は 何 寿`を作成済みにしない
- KPI/WordPress状態へ反映する場合は、`(island, mainQuery)`または固有の計画行番号で対象行を特定し、対象行だけへ記事ID・公開状態・URLを記録する。slugの一致だけで複数行を更新しない
- `deep`や`mention`を本文で実際に扱った場合でも、どの深さで答えたかをcoverage mapに残す。後から専用記事へ分割するqueryは、その時点まで未作成または言及済みとして管理する

## SERP Ownership Check Before Writing

計画ツリーの順番は、執筆候補の順番であって、そのまま本文を書き始める許可ではない。

詳細な実行手順、research保存形式、計画ツリーへの反映方法は [serp-ownership-check.md](serp-ownership-check.md) を使う。

記事制作へ入る前に、最初に着手する島だけ `SERP所有権確認` を行う。全島を一度に決め切ろうとしない。重複やカニバリの最終判断は、各記事を書く直前に近接queryだけ確認する。

確認するもの:

- 計画ツリー上で同じ島にある `記事候補` / `深掘り` / `言及` / `保留`
- 台帳上の既存slug、liveURL、親/子関係
- 着手候補query、既存所有記事query、近接する兄弟候補queryのSERP上位10件 overlap
- 既存記事で十分に答えられるか
- 新規記事にするなら、既存記事と何を分けるか

対象範囲:

- いま書こうとしているquery
- 既存slug/liveURLがある吸収先候補
- 同じ島の上位近接query 2〜5件
- その記事に入れる予定の重要な `深掘り` query

全島全queryの重複判定を一括で終わらせようとしない。遠い島や後で書く記事の最終判断は、その記事を書く直前に行う。

判断:

- 既存記事とSERPが強く重なるなら、まず既存記事のリライト/追記を優先する
- 新規記事にする場合は、既存記事側に `この記事では短く触れる` / `詳しくはこちらへ内部リンク` の境界を作る
- 補助queryは単独記事化せず、所有記事のH2/H3へ自然に入れる。本文に収まらない独立疑問がある場合だけ、短い質問ブロックを検討する
- 判断が割れるqueryは `検索結果確認` に戻し、本文を書き始めない

出力:

```md
SERP所有権確認:
- target query:
- checked existing URLs:
- checked neighbor queries:
- ownership decision: new article / rewrite existing / add section / mention only / hold
- owner slug:
- deep:
- mention:
- exclude:
- cannibal risk:
- why this can proceed:
- unresolved checks:
```

`unresolved checks` が残る場合は、本文作成ではなく追加SERP確認へ戻る。

## SERP overlap rule

query間の上位10件URL overlap を見て記事分割を決める。

- overlap 6件以上: 原則、別記事にしない。統合、同一記事H2、または片方を mention
- overlap 3〜5件: 分けてもよいが、`deep / mention / exclude` を強く固定する
- overlap 0〜2件: 別記事候補。検索意図が分かれている可能性が高い

SERP未確認の場合は `serpIndependence = unknown` とし、scoreだけで確定しない。

## Publishing order

Use the query tree and ownership checks to sequence narrow articles before a
broad hub when the evidence supports that order. Recheck existing URLs, search
intent, and internal-link paths before creating a separate page. A parent page
can be expanded after its child articles show distinct query demand and the
site has useful links to connect them.

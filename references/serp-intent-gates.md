# SERP Intent Gates

Apply these gates to substantive article research and decisions about query, intent, title strategy, or structure. Wording-only edits that preserve those decisions stay on the bounded path in `SKILL.md`.

具体 query の新規記事・既存記事改修では、title 確定・構成確定・本文作成の前にこの gate を通す。SERP を見た直後に本文や WordPress 下書きへ進まない。観察は素材であり、title 比較、構成比較、勝ち筋の構造判断まで書いて初めて記事制作に入れる。

## Gate 1: SERP answer extraction

上位ページを単に URL 列挙しない。原則として自然検索上位10件をすべて読み、少なくとも上位5件は深く見る。title / 構成 / リライト方針を確定する前に、構造 evidence をローカルの research ファイルへ保存する。

SERP は [keyword-source-research.md](keyword-source-research.md) に従って承認済みのキーワードソースから取得する。Google実画面が必要な場合だけ [serp-browser-evidence.md](serp-browser-evidence.md) を使う。

query、取得元・機能、取得日時とデータ日時、参照先、検索条件、順位範囲を記録する。Google実画面の観察時は `q` / `start` と画面の条件も別記する。会話内のメモだけで終わらせず、上位10件をresearchへ保存する。欠けるrankには理由を書き、必要な意図・構造の証拠が欠けたままtitleや構成を確定しない。

広告、AI Overview、PAA、強調スニペット、動画/画像パック、サイトリンク、同一URLの `#:~:text=` などのフラグメントリンクは、通常の organic rank と混ぜない。補助情報として読む場合も、organic rank から除外した理由を research に残す。

キーワードソースのSERPデータをGoogle実画面の観察と混同しない。実画面が必要なのに取得できない場合は、具体的な原因と不足を記録し、その画面に依存する結論だけを保留する。取得済みのソースデータによる通常調査は続けてよい。

保存すること:

- SERP snapshot:
  - query
  - date
  - primary snapshot: 承認済みキーワードソース / 機能 / UI・MCP・API・export
  - 参照URL・request ID・export path、取得日時、データ日時
  - engine / country / language / device / rank range（不明はunknown）
  - Google実画面を見た場合だけ `q` / `start` / captured time / location / personalization
  - 広告、AI Overview、PAA、動画は取得元と確認範囲を記録し、未観察を「なし」にしない
  - organic rank から除外した SERP module / duplicate fragment のメモ
- 自然検索上位10件:
  - rank
  - URL
  - page type
  - title
  - H1
  - 主要 H2/H3
  - 冒頭で即答している内容
  - CTA / 内部リンク導線
  - そのページが勝っている理由
- 10 -> 1 rank ladder:
  - 10位から6位のページに足りないもの
  - 5位から3位で増えるもの
  - 2位と1位の差
  - 1位が代表回答として選ばれている理由
- Title Top 10 Comparison:
  - 上位10件の title を横並びで比較する
  - 主語、前半語、条件語、不安語、解決語、自然さ、検索意図との距離を見る
  - 1〜3位の title がなぜ強いのか、6〜10位の title に何が足りないのかを書く
  - 自記事 title に採用する語彙と、採用しない語彙を理由付きで分ける
- Structure Top 10 Comparison:
  - 上位10件の H1/H2/H3 の順番を横並びで比較する
  - 即答位置、共通必須セクション、質問ブロックがある場合の役割、PAA、例・表・画像/ギャラリー、CTA/導線を見る
  - 1〜3位が持っていて下位が弱い構成要素を特定する
  - 記事で深く扱う要素、薄く触れる要素、内部リンクやサービスページへ逃がす要素を分ける
- Semantic depth / extractability:
  - 上位が説明している entity、属性、条件、比較軸、関係性、具体例を抜き出す
  - 自記事で冒頭即答、短い定義、比較表、手順、必要な質問ブロック、図解として抜き出しやすくする要素を決める
  - AI Overview や featured answer に使われても意味が崩れない自己完結した説明ブロックをどこに置くか決める
- Entity / brand clarity:
  - site/category/audience/distinct point を記事内で自然に回収できる場所を決める
  - 地域、対象読者、運営主体、サービス導線が検索意図から浮いていないか確認する
- Visual / diagram opportunity:
  - 比較、時系列、手順、判断基準、チェックリスト、数値差、地図性があるかを見る
  - demand / impressions がある記事では、図解・表・カスタム画像が理解を増幅するか判断する
  - intent ズレや target-query visibility 不足を画像だけで解決しようとしていないか確認する
- Top 10 -> article structure rationale:
  - 上位10件の共通必須要素
  - 採用する H2/H3 と、その根拠になった rank
  - 採用しない要素と理由
  - 親記事 / 子記事 / 内部リンク先へ逃がす要素
- Winning Structure Decision:
  - 上位10件の title / 構成比較から導いた最終 H2/H3
  - 各セクションの深さと順番
  - 冒頭で即答する内容
  - 質問ブロック（必要な場合のみ）、表、画像/ギャラリー、事例、CTA の配置
  - 内部リンク、親子記事、サービスページ、相談導線へ渡す位置
- 20 -> 30 fallen-page comparison:
  - 似たページがなぜ下がっているのか
  - 上位10に足りない主題、即答、構造、例、信頼表示、鮮度、内部導線
  - 真似してはいけない下位ページの特徴
- 横断要約:
  - title の勝ち語彙
  - 共通 H2/H3
  - 優勢な page type と page type mix
  - 上位5件に共通する深掘り要素
  - 抜き出されやすい即答/表/図解の候補
  - entity / brand clarity の補強ポイント
  - 自記事が外している可能性
  - 採用する title / 構成への反映

11〜20位と、取得可能なら20〜30位前後の類似ページを比較する。取得範囲外は理由付きWARNにし、Google実画面を一律に要求しない。page type、title、即答位置、H2/H3、CTA、信頼表示、例・表・画像の違いを見る。観察した違いと順位への影響の推測を区別する。

Research CI check:

- research ファイルがある場合は、本文・WP下書き・package 作成前に `scripts/article_ci.py` の Research CI を通す。
- CLI を使える場合は `article_ci.py --stage research --fail-on needs_evidence` を使う。
- `NEEDS_EVIDENCE` は停止条件。足りない SERP / page / GSC evidence を集め直してから進む。
- `WARN` で進む場合は、何をリスクとして残すのか、なぜ今進めるのかを research に書く。
- `PASS` または理由付き `WARN` なしに本文へ入らない。

## Gate 2: AI Overview / featured answer extraction

Google の AI Overview、強調スニペット、People Also Ask、動画要約などで標準回答が見えている場合は、補助情報で終わらせない。

抽出すること:

- 標準回答の主語
- 手順 / 型 / 定義 / 比較軸
- 使われている実語彙
- 例文やテンプレートの有無
- 自記事が必ず回収すべき要素

AI Overview が取得できない場合は、そのことを明記して通常 SERP で進める。取得できた場合は、構成の必須要素に反映する。

## Gate 3: Intent-fit comparison

構成を作る前に、次の比較を必ず行う。

```md
Query:
- <target query>

SERP standard answer:
- <上位とAI Overviewが共通して返している答え>

Our planned article:
- <自分の記事の主題>

Mismatch risk:
- <総論すぎる / 一部セクション扱い / title語彙が弱い / 例文不足 など>

Decision:
- <既存URLを寄せる / 専用記事を作る / queryを変える>
```

新規記事では `Our planned article`、既存記事リライトでは `Current article` と `Revised article` の両方を書く。

`Mismatch risk` が残る場合は、本文を書き始めない。

## Gate 4: Parent / child topic classification

title・構成・既存URL改修・分割判断の前に、この query が親トピックなのか子トピックなのかを分類する。ここを曖昧にすると、親queryに子記事をぶつけたり、子queryを不必要に広げたりして、対応が逆になる。

親子はサイト側の都合で決めない。SERP の上位ページがどの範囲まで答えているか、20〜30位の類似ページや関連 query がどこで落ちているか、検索者が本当に知りたい「次の判断」が何かで決める。

書くこと:

```md
Classification:
- parent / child / sibling / mixed / unknown

Confidence:
- high / medium / low

Evidence:
- SERP breadth:
- Rank ladder:
- Lower-page comparison:
- Fallen-page comparison 20-30:
- SERP features:
- Query variants inside top pages:
- Query variants needing separate pages:
- Volume / demand notes:
- GSC query spread if published:

Decision branch:
- <write parent first / focused child article / sibling article / merge into parent / retarget existing URL / evidence collection>

Duplication boundary:
- Parent article owns:
- Child or sibling article owns:
- Repeated only as short context:
- Do not cover here:
```

判定軸:

- 親トピック: 上位が総合ガイドで、複数の子不安をH2/H3内に回収している。
- 子トピック: 上位が具体的な1つの不安・症状・物・時期・行動に即答している。
- sibling: 上位が親の一部ではなく、別の同階層 intent として独立している。親記事からリンクするが、親子主従にしすぎない。
- mixed: 上位の解釈が割れている。仮の役割を決め、GSCや内部リンク強化後に再判断する。
- unknown: SERP evidence が足りない。titleや本文に進まない。

順番の決め方:

- 親から書く: 上位が総合ガイドで、検索者が比較・全体像・判断基準を求めている。子 query のボリュームが小さく、上位の親ページ内で十分に回収されている。
- 子から書く: 上位が狭い intent に即答しており、親記事では答えきれない独自の手順、例、条件、または本文に入らない独立した質問がある。
- 兄弟として書く: 親と読者は近いが、SERP の勝ち筋、title 語彙、CTA が別物になっている。
- 書かない/統合する: 子 query の SERP が親SERPとほぼ同じで、専用記事にすると同じ定義・比較・一般論を繰り返すだけになる。

重複を防ぐ実務ルール:

- 親記事は地図: 全体像、選択肢、判断基準、子記事への導線を持つ。
- 子記事は現地案内: 1つの具体不安・条件・行動に絞り、具体例、手順、失敗回避を厚くする。質問ブロックは本文で答えきれない独立疑問がある場合だけ使う。
- 子記事の冒頭では親の定義を1〜2文だけ回収し、厚い定義・網羅比較は親へリンクする。
- 親記事から子記事へは、検索者が次に迷う場所で文脈リンクする。子記事から親記事へは、全体像を確認したい読者向けに戻す。
- SERP が親型なのに子記事を書く場合は、なぜ子として勝てるのかを `Differentiation that does not replace must-have sections` として明記する。

## Gate 5: Title intent lock

title 案を出す前に、次を決める。

- 主行動語: 検索者が今やりたいこと
- 不安語: 検索者が避けたい状態
- 条件語: 誰向け / どんな条件か
- 解決語: 例文 / 手順 / 判断 / 比較 / 対策

title は、原則として主行動語を前半に置く。条件語を入れる場合でも、主 query の行動語を後ろへ追いやらない。

## Gate 6: Structure parity

H2/H3 を確定する前に、上位ページの共通必須要素と自記事の差別化要素を分ける。

```md
Common must-have sections:
- <上位が共通して持つ定義/手順/例文/注意点/必要な質問ブロック>

Our differentiation:
- <読者・地域・職種・体験・導線などで上乗せする要素>

Do not replace:
- <差別化で置き換えてはいけない必須要素>
```

差別化要素は、共通必須要素の代わりにしない。必須要素を満たしたうえで追加する。

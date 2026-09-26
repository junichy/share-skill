# Article Production

本文、slug、package を作る時に読む。

## Default writing stance

- 口調: 親しみやすい `です・ます`
- 本文: ストーリー、具体例、問いかけを使う
- 専門語: かみ砕いて説明する
- キーワード: 詰め込まず自然配置する
- 見出し: SEO 重視
- 本文: 読者体験重視
- まとめ: 次の行動を明確にする

本文内の過剰な箇条書きは避ける。

## Target length math

競合文字数が取れる場合:

- 上位3記事の文字数を取得
- `avg` `max` `min` を算出
- `base = max(round(avg * 1.25), max_len)`

意図別調整:

- informational: `* 1.2`
- how-to: `* 1.0 - 1.1`
- troubleshooting: `* 1.2`
- comparison: `* 1.3`

フォールバック:

- 競合文字数が取れない場合は 3,500-4,500 字

## Drafting

- 段落中心で書く
- 新規記事・全面改稿では最初のH2より前に300字程度の導入文を置き、検索者の不安や行動にすぐ答える。正確に300字へ水増ししない
- 会話素材は質問・回答の形式にせず、短い段落の本文にする。具体例は確認できたものだけ使う
- 目標文字数の +/-5% 以内を目安に仕上げる
- まとめは 250-350 字目安

## Slug

- title 承認後の slug は Codex が site rule に従って自動決定してよい
- パーマリンク案を 2-3 個出し、推奨案を1つ示す
- site-specific な slug language rule がある場合は project profile / repo instructions を優先する

## Final Package

Final Package には最低限次を含める。

- 要件サマリ
- target query / search intent
- SERP answer extraction
- AI Overview / featured answer elements if present
- Intent-fit comparison
- 勝ち型分析
- 目標文字数の根拠
- 関連キーワード配置戦略
- ペルソナ
- 採用 title
- 構成
- 本文
- パーマリンク
- 内部リンク方針
- 保存先

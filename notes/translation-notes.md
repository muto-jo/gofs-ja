# 翻訳メモ

翻訳中に相談した疑問・解釈・最終的な判断の記録。

- 翻訳対象: [MobilityData/gofs](https://github.com/MobilityData/gofs) `README.md`, `reference.md`
- 原文コミット: `bd0f124eb6f0a81cdae6c19033039fd26d70fca4`（2026-09-30）
- 訳語の一覧は [glossary.md](glossary.md)

## タグ

各記録に 1 つ付ける。掲載先の判断に使う。

| タグ | 内容 | 掲載 |
|---|---|---|
| リファレンス誤り | リファレンス自体のミス。リファレンスの時点で誤っているもの | 最終的に MobilityData に Issue を立てる。記事・GitHub に注意として載せる |
| 翻訳方針 | 翻訳するにあたって確認を要した点。リファレンスの解釈に関わるもの | 記事・GitHub に載せる |
| プロジェクト方針 | この翻訳・サンプル作成プロジェクトでの確認事項 | 載せない |

## 書式

```markdown
### T-番号 見出し（短く）
- タグ: リファレンス誤り | 翻訳方針 | プロジェクト方針
- 対象箇所: reference.md「節名」／ 原文の該当文
- 疑問:
- 検討・解釈:
- 結論:
- 状態: 未決 | 決定（YYYY-MM-DD）
```

---

## 記録

### T-001 見出しを訳すと目次のリンクが切れる
- タグ: プロジェクト方針
- 対象箇所: reference.md「Table of Contents」と、本文中の `#document-conventions` などのページ内リンク
- 疑問: 見出しを日本語にすると GitHub が生成するアンカーが変わり、原文のページ内リンクが切れる。どう扱うか
- 検討・解釈: 案A 見出しを日本語にしてリンク先を新アンカーに書き換える／案B「用語の定義（Term Definitions）」のように英語を併記する／案C ファイル名の見出し（`gofs.json` など）は原文のまま残す。案C は案A・B のどちらとも両立する
- 結論: 案A＋HTML アンカー。見出しは日本語のみにし、直前に原文と同じアンカーを `<a id="term-definitions"></a>` の形で置く。ページ内リンクの `#...` は原文のまま変えない。ファイル名の見出し（`### gofs.json` など）は訳さない
- 理由: 原文と訳文でリンクが同じになり照合しやすい。外部から `reference.md#zonesjson` のように原文のアンカーで張られたリンクも訳文でそのまま使える
- 状態: 決定（2026-10-27）

### T-002 gofs.json の `language` フィールドと例の構造が一致しない
- タグ: リファレンス誤り
- 対象箇所: reference.md「gofs.json」
- 疑問: フィールド表では `data` の直下に `language` と `feeds` があるように読めるが、例では `data` の下が `"en"`, `"fr"` の言語コードをキーにしたオブジェクトになっている（GBFS v2 系の構造）。どちらに従うべきか
- 検討・解釈: 翻訳としては原文どおり訳し、訳注で食い違いを指摘する。サンプル作成時にどちらの構造を採るかは、`upstream/gofs/schema/gofs.json` の定義も確認して実装メモで決める
- 結論:
- 状態: 未決

### T-003 ゾーンのポリゴンの頂点の向きが RFC 7946 と逆に書かれている
- タグ: リファレンス誤り
- 対象箇所: reference.md「zones.json」`geometry` の説明 ／ "a clockwise arrangement of points defines the area enclosed by the polygon, where pickup and drop off MAY occur"
- 疑問: RFC 7946 §3.1.6 は外周リングを反時計回り（穴は時計回り）としている。GOFS の記述は「時計回り = 乗降できる範囲」で逆に読める。しかも同じ節の例（zoneA）の外周は反時計回りで、本文と例が食い違っている。また `geometry` の型は GeoJSON Polygon だけで、MultiPolygon は書かれていない
- 検討・解釈: 翻訳は原文どおりにし、訳注で RFC 7946 および例との違いを指摘する。ポリゴン作成時にどちらの向きにするか、飛び地のある提供エリアを複数ゾーンに分けるかは実装メモで決める。`tools/validate.py` は向きをエラーにせず情報として表示する
- 結論:
- 状態: 未決

### T-004 表の Presence 列を訳すか
- タグ: プロジェクト方針
- 対象箇所: reference.md の全フィールド表の Presence 列（REQUIRED 59 回・OPTIONAL 51 回・Conditionally REQUIRED 14 回）
- 疑問: 英語のまま残すか、日本語にするか
- 検討・解釈: 英語のままだと原文と照合しやすく RFC 2119 とも対応が明確。日本語にすると一目で読める。gtfs.org の GTFS 日本語版は「必須／任意／条件付きで必須」と訳している
- 結論: 日本語にする。訳語は gtfs.org 日本語版に揃えて「必須／任意／条件付きで必須」（glossary.md）
- 状態: 決定（2026-10-27）

### T-005 本文中の RFC 2119 キーワードの書き方
- タグ: プロジェクト方針
- 対象箇所: reference.md 全体の MUST / SHOULD / MAY など
- 疑問: 日本語だけにするか、英語を残すか
- 検討・解釈: 日本語だけだと要求の強さが訳語に左右される。英語のままだと読みにくい
- 結論: 「〜しなければならない（MUST）」のように日本語に英語を併記する。RFC 2119 に無い FORBIDDEN も「禁止（FORBIDDEN）」と併記する
- 状態: 決定（2026-10-27）

### T-006 rider と user の訳し分け
- タグ: 翻訳方針
- 対象箇所: reference.md・README.md の rider（33 回）・user（24 回）
- 疑問: どちらも「利用者」にまとめるか、訳し分けるか
- 検討・解釈: 原文はほぼ同じ意味で混ぜて使っているように見える。gtfs.org 日本語版は rider を「乗客」「ライダー」で揺れている
- 結論: 訳し分ける。rider は「乗客」、user は「利用者」。原文の語の違いを訳文でも追えるようにする。予約の文脈で「乗客」が不自然な箇所は個別に相談する
- 状態: 決定（2026-10-27）

### T-007 例・クエリ・レスポンスの見出しにはアンカーを置かない
- タグ: プロジェクト方針
- 対象箇所: reference.md の「##### Example:」「###### Query:」「###### Response:」など
- 疑問: T-001 の方針では見出しごとに原文のアンカーを置くが、例の見出しにも必要か
- 検討・解釈: これらは同名の見出しが多数あり、GitHub が `#example-3` のように連番を振るだけで、原文からも外部からもリンクされていない
- 結論: 「例:」「クエリ:」「レスポンス:」の見出しにはアンカーを置かない
- 状態: 決定（2026-10-28）

### T-008 README の相対リンク `schema/` の扱い
- タグ: プロジェクト方針
- 対象箇所: README.md「GOFS JSON schema」／ `[here](schema/)`
- 疑問: 訳文は `ja/` にあるため、相対リンクのままだとリンク切れになる。submodule（`upstream/gofs/schema/`）への相対リンクも GitHub 上では辿れない
- 結論: 原文リポジトリの絶対 URL（`https://github.com/MobilityData/gofs/tree/main/schema`）に置き換えた。それ以外の URL は原文のまま
- 状態: 決定（2026-10-28）

### T-009 本文に訳注を入れた箇所
- タグ: プロジェクト方針
- 対象箇所: reference.md 全体
- 疑問: 原文の食い違いや誤りのうち、どこまで本文に訳注として書くか
- 検討・解釈: 実装者が原文どおりに作ると誤ったデータになるもの、または読み手の役に立つ日本向けの補足に限って本文に入れ、軽微な誤記は T-010 に記録するだけにした
- 結論（初稿）: 本文に入れた訳注は次の 11 か所。リファレンス誤りにあたるものは個別の記録（括弧内の番号）に分けた
  1. 文書の規約: キーワードの訳し方（本訳の方針）
  2. 存在条件: FORBIDDEN が定義の一覧に無い（T-019）
  3. Phone number: 日本の電話番号の例（`+81312345678`）
  4. Currency code: 日本円は JPY
  5. データセットのファイル: `booking_type=real-time` は `booking_type=0` を指すと解される（T-014）
  6. gofs.json: フィールド表と例の構造の食い違い（T-002）
  7. zones.json: ポリゴンの向きが RFC 7946 および例と逆（T-003）
  8. operating_rules.json: `vehicle_type_id` が必須のため `vehicle_types.json` も実質必須（T-015）
  9. booking_rules.json: 例が JSON として不正（`}` が 1 つ多い）で、必須フィールドも欠けている（T-016）
  10. realtime_booking: `estimated_travel_cost` は `travel_cost` を指すと解される（T-017）
  11. ディープリンク: 例のパラメータ名（`pick_up_time`）と時刻の単位（ミリ秒）が表と食い違う（T-018）
  - README.md にも 1 か所: パラトランジットの補足（T-022）
- 結論（2026-10-28 確認）: 一覧の訳注はすべてこのまま残す。日本向けの補足（3. 電話番号、4. JPY、README のパラトランジット）も訳注として入れてよい。リファレンス誤りにあたるものは個別の記録で扱う
- 状態: 決定（2026-10-28）

### T-010 原文の軽微な誤記（訳注にせず記録のみ）
- タグ: リファレンス誤り
- 対象箇所と内容:
  - フィールドの型 Enum の例: `boarding_inacessible`（正しくは `boarding_inaccessible`）。コード部分なので訳文でも原文のまま
  - フィールドの型 ID の例: 「`id` MUST be unique among zones」だが、ゾーンのフィールド名は `zone_id`
  - 出力形式: 「the feed confirms」は conforms（準拠する）の誤りと解して訳した
  - 出力形式の例: 共通ヘッダーの例だが、中身は system_information.json の内容になっている
  - calendars.json `days` の例: `"sat, "sun"` の引用符が欠けている。コード部分なので原文のまま
  - wait_time のリクエストパラメータ表: `brand_id` の行の型が `ID |  Array` となっており、列が 1 つ多い。原文のまま残した
  - booking_rules.json `from_zone_ids`: 「that cover the area of the wait time update（待ち時間の更新対象エリア）」は、他の節からの転記と思われる。意味は乗車ゾーンと解される。直訳のまま
  - realtime_booking: 「At least of one」（At least one の誤り）、「the the same」「adresses」
  - フィールドの型 Time: 「trip schedule begins」は GTFS からの転記と思われる。「運行スケジュールが始まる日」と訳した
- 結論: 原文の誤りとして記録するだけにし、MobilityData への報告（Issue）は別途検討する
- 状態: 決定（2026-10-27）

### T-011 MAY NOT の訳し分け
- タグ: 翻訳方針
- 対象箇所: gofs.json `url`「MAY NOT be defined in the `file_name.json` format」／ zones.json `geometry`「pickup and drop off MAY NOT occur」
- 疑問: RFC 2119 に MAY NOT は無い。文脈によって意味が違う
- 検討・解釈: gofs.json では「その形式でなくてもよい」（任意）、zones.json では「乗降できない」（禁止）の意味
- 結論（初稿）: gofs.json は「定義されていなくてもよい（MAY NOT）」、zones.json は「行うことができない（MAY NOT）」と訳し分けた
- 結論（2026-10-27 更新）: MAY NOT の訳語は「〜しなくてもよい（MAY NOT）」とする（glossary.md）。gofs.json はこの訳語どおり。zones.json の 1 か所は、この訳語にすると「乗車と降車を行わなくてもよい領域」となり、原文が意図する「乗降できない領域」と逆の意味に読めるため、例外として「行うことができない（MAY NOT）」とする
- 状態: 決定（2026-10-27）

### T-012 小文字の must / should
- タグ: 翻訳方針
- 対象箇所: Color「must not be included」、wait_time「must be made」「Should be empty」、ディープリンク「should support」など
- 疑問: 小文字のものも RFC 2119 のキーワードとして扱うか
- 検討・解釈: RFC 8174 では大文字の場合だけキーワードとしての意味を持つ。ただし原文は大文字・小文字を厳密に使い分けているようには見えない
- 結論（初稿）: 小文字は英語を併記せず、普通の日本語（「〜しなければならない」「〜すべきである」）で訳した。この方針は「文書の規約」の訳注にも書いた
- 状態: 決定（2026-10-28）

### T-013 Fare オブジェクトの `amount` と `interval` の関係が読み取りにくい
- タグ: 翻訳方針
- 対象箇所: fares.json「"Fares" オブジェクトの構造」と例 1
- 疑問: `amount` は「親キーの 1 単位あたり」（例: 1km あたり）の額とされ、`interval` は課金する刻み幅とされる。例 1 の「1km あたり 3.30 CAD を 250m ごとに課金」は、250m ごとに 0.825 CAD（= 3.30 × 0.25）ずつ加算されると読める。日本のタクシー運賃（初乗り○m まで○円、以後○m ごとに○円）をどう表すかに直結する
- 検討・解釈: 上の読み方（250m ごとに 3.30 × 0.25 = 0.825 CAD を加算）で正しいと判断した。`amount` を「1 区間（`interval`）あたりの額」ではなく「親キーの 1 単位あたりの額」で書かせるため、非直感的で分かりにくい。例えば日本のタクシーの「255m ごとに 100 円加算」は、`interval: 0.255` に対して `amount` を 1km あたりの額（100 ÷ 0.255 = 392.156…円）で書くことになり、割り切れない
- 結論: 解釈は上のとおり。日本のタクシー運賃をどう表現するかは、サンプル作成時に実装メモで詰める。分かりにくさについては MobilityData の Slack で意見するか？（Issue はまだ立てない）
- 状態: 決定（2026-10-27）。表現方法は実装メモに引き継ぐ

### T-014 `booking_type=real-time` という値は定義されていない
- タグ: リファレンス誤り
- 対象箇所: reference.md「Dataset Files」表の `wait_time` と `realtime_booking` の行 ／ "at least one `booking_rule` is `booking_type=real-time`"
- 疑問: booking_rules.json では `booking_type` は数値の列挙値（`0` リアルタイム予約、`1` 事前通知による当日予約まで、`2` 前日予約まで）として定義されており、`real-time` という値は無い。また `booking_rule`（単数形）というファイルやフィールドも無い
- 検討・解釈: `booking_type=0` を指すと解される
- 結論: 訳文は原文どおりにし、表の直後に訳注で `booking_type=0` を指すと解されることを書いた
- 状態: 決定（2026-10-27）

### T-015 `vehicle_type_id` が必須なので `vehicle_types.json` が「条件付きで必須」にならない
- タグ: リファレンス誤り
- 対象箇所: reference.md「operating_rules.json」`vehicle_type_id`（REQUIRED, Array）／「Dataset Files」および「vehicle_types.json」の "This file is REQUIRED if any vehicle types are referenced in `operating_rules.json`"
- 疑問: 運行ルールは常に `vehicle_type_id` を持つことになるため、「車両タイプが参照されている場合に必須」という条件が常に成り立ち、`vehicle_types.json` は実質的に常に必須になる。どちらかの存在条件が意図と違うと思われる（`vehicle_type_id` を任意にするつもりだった可能性がある）。あわせて、フィールド名は単数形（`vehicle_type_id`）なのに型が Array になっている
- 検討・解釈: 原文のままでは、車両タイプを区別しないサービスでも `vehicle_types.json` を作る必要がある
- 結論: 訳文は原文どおりにし、表の直後に訳注で「実質的に常に必須となる」ことを書いた。サンプルでの扱いは実装メモで決める
- 状態: 決定（2026-10-27）

### T-016 booking_rules.json の例が JSON として不正で、必須フィールドも欠けている
- タグ: リファレンス誤り
- 対象箇所: reference.md「booking_rules.json」の例
- 疑問:
  - 末尾の閉じ括弧 `}` が 1 つ多く、JSON としてパースできない
  - 2 つ目のルールは `booking_type: 2` だが、`booking_type=2` で必須の `prior_notice_last_day` が無い（`prior_notice_last_time` だけがある。`prior_notice_last_time` は `prior_notice_last_day` が定義されている場合以外は禁止）
  - 同じルールで `prior_notice_start_day` を指定しているのに、その場合に必須の `prior_notice_start_time` が無い
  - 1 つ目のルールの `"to_zone_ids": null` は、型が Array とされていることと合わない（省略すべきか null を許すのかが書かれていない）
- 検討・解釈: 例をそのまま写すと検証に通らないデータになる
- 結論: 訳文では例（コード）は原文のまま残し、例の直前に訳注で JSON として不正なことと必須フィールドの欠落を書いた（`to_zone_ids: null` の件は訳注に含めていない）
- 状態: 決定（2026-10-27）

### T-017 realtime_booking の `estimated_travel_cost` は存在しないフィールド
- タグ: リファレンス誤り
- 対象箇所: reference.md「realtime_booking」`travel_cost_currency` ／ "Currency of the `estimated_travel_cost`. REQUIRED if `estimated_travel_cost` is provided."
- 疑問: レスポンスに `estimated_travel_cost` というフィールドは無く、定義されているのは `travel_cost`
- 検討・解釈: `travel_cost` を指すと解される（改名の際の直し漏れと思われる）
- 結論: 訳文は原文どおりにし、表の直後に訳注で `travel_cost` を指すと解されることを書いた
- 状態: 決定（2026-10-27）

### T-018 ディープリンクの例のパラメータ名と時刻の単位が表と食い違う
- タグ: リファレンス誤り
- 対象箇所: reference.md「deeplink with query params」の表と例
- 疑問:
  - 表のパラメータ名は `pickup_time` だが、例では `pick_up_time` になっている（`drop_off_time` は一致）
  - 表では時刻は Timestamp 型（Unix エポックからの秒数）だが、例の値 `1726173300000` / `1726173600000` は 13 桁でミリ秒になっている
- 検討・解釈: 表の定義（`pickup_time`、秒）が正しく、例が誤っていると解される
- 結論: 訳文では例（コード）は原文のまま残し、例の直前に訳注で食い違いを書いた
- 状態: 決定（2026-10-27）

### T-019 FORBIDDEN が存在条件の一覧で定義されていない
- タグ: リファレンス誤り
- 対象箇所: reference.md「Presence」（REQUIRED / OPTIONAL / Conditionally REQUIRED の 3 つだけを定義）／ wait_time・booking_rules.json のフィールドの説明（"FORBIDDEN otherwise" など、計 11 回）
- 疑問: 本文の条件の説明では FORBIDDEN が使われているが、「Presence」の一覧にも RFC 2119 のキーワードにも含まれておらず、意味が定義されていない。同様に「Conditionally FORBIDDEN」に相当する条件（例: `prior_notice_start_day` は「`booking_type=0` の場合は禁止、それ以外は任意」）も、存在条件の区分としては表せず、表の Presence 列では「任意」などになっている
- 検討・解釈: GTFS の Presence の定義（Forbidden: そのフィールドやファイルを含めてはならない）と同じ意味と解される
- 結論: 訳文は「禁止（FORBIDDEN）」と訳し、「必須性」の一覧の直後に訳注で、一覧に定義が無いことと、GTFS と同じ意味と解されることを書いた（T-005 の訳語も参照）
- 状態: 決定（2026-10-27）

### T-020 price / cost の訳語を「価格」にする
- タグ: 翻訳方針
- 対象箇所: README.md「accurate pricing」／ reference.md「operating_rules.json」`fare_id`、「fares.json」の各フィールドと例 3、「realtime_booking」の冒頭（price 6 回・pricing 3 回・cost 10 回程度）
- 疑問: 初稿では「料金」としていたが、fare（運賃）との違いが訳文で分かりにくい。また鉄道では「運賃」と「料金」（特急料金など）は別のものを指すので、「料金」は誤解を招く
- 検討・解釈: price の直訳は「金額」だが、訳文としてやや不自然。GOFS では、価格の計算ルール（キロあたり・分あたりなど）があり、それによって運賃が決まるという関係になっている
- 結論: price / cost / pricing は「価格」「価格設定」とする（基本価格、サービス価格、価格情報、組み合わせ価格、延長価格など）。fare cost / fare amount は「運賃額」、surcharge は「追加料金」のまま
- 状態: 決定（2026-10-27）

### T-021 表の Presence を「必須性」と訳す
- タグ: プロジェクト方針
- 対象箇所: reference.md「Presence」の節の見出し、目次、すべての表の Presence 列の見出し（計 21 か所）
- 疑問: 初稿の「存在条件」は分かりにくい
- 検討・解釈: この列は必須・任意・条件付きで必須のどれにあたるかを示すもの。gtfs.org 日本語版の「存在」も意味が通りにくい
- 結論: 「必須性」とする。節の見出しは「必須性」、本文は「必須性の区分は次のとおり」とした。アンカーは原文どおり `#presence`
- 状態: 決定（2026-10-27）

### T-022 paratransit を訳注で補足する
- タグ: 翻訳方針
- 対象箇所: README.md「Examples of supported services include ... paratransit」
- 疑問: 「パラトランジット」は日本ではなじみが薄く、GOFS が対象とするサービスの範囲が伝わりにくい
- 結論: 訳語は「パラトランジット」のままとし、訳注で「主に障害などにより路線バスや鉄道の利用が難しい人を対象とした、予約制の送迎サービス。日本の福祉有償運送や福祉タクシーなどの STS（スペシャル・トランスポート・サービス）に近い」と補足した
- 状態: 決定（2026-10-27）

### T-023 Fare オブジェクトの `start` / `end` が整数型で、小数の距離を書けない
- タグ: 翻訳方針
- 対象箇所: reference.md「fares.json」「"Fares" オブジェクトの構造」の `start` / `end`（型は Non-negative Integer）
- 疑問: `interval` は Float だが、`start` と `end` は Non-negative Integer とされている。親キーが `kilometer` の場合、区間の境目は整数のキロメートルでしか書けない。例えば日本のタクシーの「初乗り 1.096km まで」の `start: 1.096` は型に合わない（原文の例はいずれも整数の 10・20・25 なので問題が表に出ない）
- 検討・解釈: 原文どおりに読めば、小数の距離・時間を区間の境目にできない。T-013（`amount` は親キーの 1 単位あたりの額）とあわせて、日本のタクシー運賃を正確に表すのが難しい。対応の候補は、型に反して小数を書く／整数に丸めて近似する／`rider`（基本価格）と `kilometer` の組み合わせで別の表し方を探す、など
- 結論: 解釈は上のとおり（整数のみ）。サンプルでどう表現するかは実装メモで決める。T-013 とあわせて MobilityData に意見するかも検討する
- 状態: 決定（2026-10-28）。表現方法は実装メモに引き継ぐ

### T-024 curb-to-curb を訳注で補足する
- タグ: 翻訳方針
- 対象箇所: README.md「Future GOFS extensions may support on-demand services: operated from curb-to-curb, stop-to-stop, or door-to-door」
- 疑問: 「カーブ・トゥ・カーブ」は日本ではなじみが薄く、stop-to-stop・door-to-door との違いが伝わりにくい
- 検討・解釈: curb は縁石・路肩。デマンド型交通やパラトランジットの用語で、利用者が指定した場所の前の路肩で乗降する方式を指す（運転手は車両の乗り降りまでで、建物の玄関までは介助しない）。stop-to-stop は決まった停留所で乗降する方式、door-to-door は運転手が建物の玄関と車両のあいだの移動も介助する方式。米国の ADA パラトランジットでは curb-to-curb が基本で、door-to-door は必要に応じて提供されることが多い
- 結論: 訳語は「カーブ・トゥ・カーブ（curb-to-curb）」とし、箇条書きの項目の直後の行に「（訳注: curbは縁石、路肩。利用者の指定する場所の路肩で乗降する方式）」と補足した。項目の文中に入れると読みにくくなるため、文の後ろに置いた
- 状態: 決定（2026-10-29）

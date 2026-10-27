# 訳語集

翻訳で使う訳語の一覧。状態が「案」のものは Claude の初期提案で、確認・修正したら「決定」にする（2026-10-27 に全件確認済み）。
変更したときは `ja/` 内の該当箇所もあわせて直す。
参考: [gtfs.org の GTFS Schedule リファレンス日本語版](https://gtfs.org/ja/documentation/schedule/reference/)（2026-10-27 確認）。GTFS と共通する語はなるべくこれに揃える。

## RFC 2119 キーワード（本文中）

本文中では日本語に英語を併記する（T-005）。

| 原語 | 訳語 | 状態 | 備考 |
|---|---|---|---|
| MUST / REQUIRED / SHALL | 〜しなければならない（MUST） | 決定 |  |
| MUST NOT / SHALL NOT | 〜してはならない（MUST NOT） | 決定 |  |
| SHOULD / RECOMMENDED | 〜すべきである（SHOULD） | 決定 |  |
| SHOULD NOT | 〜すべきではない（SHOULD NOT） | 決定 |  |
| MAY / OPTIONAL | 〜してもよい（MAY） | 決定 |  |
| MAY NOT | 〜しなくてもよい（MAY NOT） | 決定 | RFC 2119 に無い語。zones.json の「pickup and drop off MAY NOT occur」だけは意味上「乗降できない」なので、例外として「行うことができない（MAY NOT）」とする（T-011） |
| FORBIDDEN | 禁止（FORBIDDEN） | 決定 | RFC 2119 に無い語（GTFS 由来）。本文の条件説明に 11 回。例: 「それ以外の場合は禁止（FORBIDDEN）」 |

## 表の Presence 列

表の Presence 列は日本語にする（T-004）。訳語は gtfs.org の日本語版に揃える。

| 原語 | 訳語 | 状態 | 備考 |
|---|---|---|---|
| REQUIRED | 必須 | 決定 | 59 回 |
| OPTIONAL | 任意 | 決定 | 51 回 |
| Conditionally REQUIRED | 条件付きで必須 | 決定 | 14 回 |

## 用語

| 原語 | 訳語 | 状態 | 備考 |
|---|---|---|---|
| on-demand service | オンデマンドサービス | 決定 |  |
| feed | フィード | 決定 |  |
| system | システム | 決定 | 1 つのフィードが表すサービス全体 |
| data producer / publisher | データ提供者 | 決定 |  |
| consuming application / data reuser | データ利用アプリケーション／データ利用者 | 決定 |  |
| rider | 乗客 | 決定 | 33 回。user と訳し分ける（T-006） |
| user | 利用者 | 決定 | 24 回（T-006） |
| customer | カスタマー | 決定 | 原文では customer service の 3 回のみ →「カスタマーサービス」。「顧客」より日本語として自然 |
| auto-discovery | 自動検出 | 決定 |  |
| zone | ゾーン | 決定 |  |
| intra-zone / inter-zone trip | ゾーン内移動／ゾーン間移動 | 決定 |  |
| operating rule | 運行ルール | 決定 |  |
| calendar | カレンダー | 決定 |  |
| fare | 運賃 | 決定 |  |
| wait time | 待ち時間 | 決定 |  |
| booking | 予約 | 決定 |  |
| booking rule | 予約ルール | 決定 | gtfs.org 日本語版に合わせる |
| real-time booking | リアルタイム予約 | 決定 | gtfs.org 日本語版の booking_type=0 の訳に合わせる |
| service brand | サービスブランド | 決定 |  |
| vehicle type | 車両タイプ | 決定 |  |
| pickup / drop off | 乗車／降車 | 決定 | gtfs.org 日本語版と同じ。「迎車」とするかは文脈次第 |
| ridehail | 配車サービス | 決定 |  |
| microtransit | マイクロトランジット | 決定 |  |
| paratransit | パラトランジット | 決定 | README に訳注で補足（福祉有償運送・福祉タクシーなどの STS に近い）（T-022） |
| deeplink | ディープリンク | 決定 |  |
| service day | 運行日 | 決定 | フィールドの型 Date・Time |
| operator | 運行事業者 | 決定 | gtfs.org の agency の訳「交通事業者」とは区別した |
| price / cost / pricing | 価格／価格設定 | 決定 | 価格の計算ルールがあり、それで運賃（fare）が決まるという関係で訳す。base price / base cost は「基本価格」。fare cost / fare amount は「運賃額」（T-020） |
| surcharge | 追加料金 | 決定 | luggage の説明の 1 か所のみ |
| order（ordered in real time） | 配車依頼（リアルタイムに配車依頼できる） | 決定 | README |
| private / shared trips | 個別の乗車／相乗りの乗車 | 決定 | README |
| free-floating | 乗り捨て型（フリーフローティング） | 決定 | README |
| query / dynamic query | クエリ／動的クエリ | 決定 |  |
| prior notice | 事前通知 | 決定 | gtfs.org 日本語版に合わせる |
| landing page | ランディングページ | 決定 |  |

## 表の見出し

| 原語 | 訳語 | 状態 | 備考 |
|---|---|---|---|
| Field Name | フィールド名 | 決定 |  |
| File Name | ファイル名 | 決定 |  |
| Param | パラメータ | 決定 |  |
| Presence | 必須性 | 決定 | 必須・任意・条件付きで必須のどれかを示す列なので「必須性」。gtfs.org 日本語版の「存在」や「存在条件」は分かりにくい（T-021） |
| Type | 型 | 決定 | 列の値（Array, String など）は原文のまま |
| Description | 説明 | 決定 |  |
| Defines | 定義 | 決定 | gofs_versions.json の表だけ原文がこの見出し |

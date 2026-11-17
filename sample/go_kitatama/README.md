# GO（北多摩交通圏）サンプル

タクシー配車アプリ「GO」の公開情報をもとに、北多摩交通圏で通常のタクシーを「今すぐ呼ぶ」場合を GOFS で表したサンプルです。

> [!NOTE]
> 非公式のサンプルであり、GO株式会社が提供する公式のフィードではありません。運賃などは作成時点の公開情報によるもので、最新の正確な情報は [GO 公式サイト](https://go.goinc.jp/) を確認してください。

## 内容

| ファイル | 内容 |
|---|---|
| [gofs.json](gofs.json) | 自動検出ファイル（言語 `ja`） |
| [gofs_versions.json](gofs_versions.json) | 利用可能なバージョンの一覧（1.0 のみ） |
| [system_information.json](system_information.json) | サービス名「GO（北多摩交通圏）」、運行事業者「GO株式会社」 |
| [service_brands.json](service_brands.json) | サービスブランド「GO（今すぐ呼ぶ）」（`go_regular`） |
| [vehicle_types.json](vehicle_types.json) | 車両タイプ「普通車」（`futsu`） |
| [zones.json](zones.json) | 乗車ゾーン「北多摩交通圏」（15 市）と降車ゾーン「東京都（島しょ部を除く）」 |
| [operating_rules.json](operating_rules.json) | 北多摩→北多摩、北多摩→東京都の 2 ルール（毎日・24 時間） |
| [calendars.json](calendars.json) | 毎日（2026-11-17〜2027-11-16） |
| [fares.json](fares.json) | 迎車料金 600 円（`rider`）、初乗運賃 1000m まで 500 円、以後 211m ごとに 100 円 |
| [booking_rules.json](booking_rules.json) | リアルタイム予約（`booking_type: 0`） |
| [wait_time.json](wait_time.json) | `wait_time` のレスポンス例（待ち時間 7 分） |
| [realtime_booking.json](realtime_booking.json) | `realtime_booking` のレスポンス例（立川駅→国分寺駅を想定。待ち時間 7 分、所要時間 18 分、推定運賃 4,000 円） |

`wait_time` と `realtime_booking` は本来、乗車地などをクエリで指定して問い合わせる動的なエンドポイントです。このサンプルでは、レスポンスの例を静的なファイルとして置いており、クエリにかかわらず同じ内容になります。値は例として決めたものです。

## 表していないこと

- 迎車料金が呼ぶタクシー会社によって異なること（`rider` には小平市周辺の会社の 600 円＝迎車料金 500 円＋アプリ手配料 100 円を入れた）
- 時間距離併用運賃（低速走行・停止中の時間による加算）、深夜早朝割増、予約料金
- 東京都外や島しょ部への移動
- service_brands.json の `brand_color` / `brand_text_color`（仕様では任意。原文の JSON スキーマでは必須になっているため、スキーマ検証では NG になる）

仕様の解釈や判断の経緯は [notes/implementation-notes.md](../../notes/implementation-notes.md)（I-004 以降）にまとめています。

## 出典

- 運賃・対象市: GO 公式サイト「[東京都のタクシー料金](https://go.goinc.jp/search/tokyo)」（2026-11-17 確認）
- 迎車料金・アプリ手配料: GO サポート＆ガイド「[アプリ手配料の対象エリア・タクシー会社について](https://support.go.goinc.jp/hc/ja/articles/25883285712281)」（2026/11/16 時点の記載、2026-11-17 確認）
- ゾーンの境界: 出典：国土数値情報（行政区域データ）（国土交通省）（https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2026.html ）を加工して作成。2026年1月1日時点のデータ。CC BY 4.0
  - 加工方法: 市区町村の結合、東京湾の埋立地など飛び地の往復線による接続（1ha 未満の飛び地・穴は除外）、許容誤差 10m の簡略化（[tools/build_zones.py](../../tools/build_zones.py)）

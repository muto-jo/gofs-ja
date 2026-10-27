> [!NOTE]
> これは [GOFS](https://github.com/MobilityData/gofs) の `reference.md` の**非公式**日本語訳である。MobilityData による公式の翻訳ではなく、仕様の正本は原文である。
> - 原文: https://github.com/MobilityData/gofs/blob/bd0f124eb6f0a81cdae6c19033039fd26d70fca4/reference.md
> - 翻訳日: 2026-10-27（初稿）
> - 原文は [Apache License 2.0](../LICENSE) で公開されており、本訳はその翻訳（改変）である
> - 訳語と翻訳時の判断は [notes/](../notes/) を参照。「訳注」は訳者による補足であり、原文には無い

<a id="general-on-demand-feed-specification-reference"></a>
## General On-Demand Feed Specification リファレンス

このドキュメントは、GOFS データセットを構成するファイルの形式と構造を定義する。

<a id="table-of-contents"></a>
## 目次

1. [文書の規約](#document-conventions)
   - [用語の定義](#term-definitions)
   - [必須性](#presence)
   - [フィールドの型](#field-types)
2. [データセットのファイル](#dataset-files)
3. [ファイルの要件](#file-requirements)
   - [自動検出](#auto-discovery)
   - [バージョン管理](#versioning)
   - [ローカライズ](#localization)
   - [出力形式](#output-format)
4. [フィールドの定義](#field-definitions)
   - [gofs.json](#gofsjson)
   - [gofs_versions.json](#gofs_versionsjson)
   - [system_information.json](#system_informationjson)
   - [service_brands.json](#service_brandsjson)
   - [vehicle_types.json](#vehicle_typesjson)
   - [zones.json](#zonesjson)
   - [operating_rules.json](#operating_rulesjson)
   - [calendars.json](#calendarsjson)
   - [fares.json](#faresjson)
   - [wait_time](#wait_time)
   - [booking_rules.json](#booking_rulesjson)
   - [realtime_booking](#realtime_booking)



<a id="document-conventions"></a>
## 文書の規約

このドキュメントにおけるキーワード "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY"、"OPTIONAL" は、[RFC 2119](https://tools.ietf.org/html/rfc2119) に記述されているとおりに解釈されるものとする。

> 訳注: 本訳では、これらのキーワードを「〜しなければならない（MUST）」「〜すべきである（SHOULD）」「〜してもよい（MAY）」のように、日本語に原文の英語を併記して示す。小文字の must / should などは RFC 2119 のキーワードとしては扱わず、英語を併記しない。

<a id="term-definitions"></a>
### 用語の定義

* JSON - [JavaScript Object Notation](https://www.w3schools.com/js/js_json_datatypes.asp) は、データを保存・転送するための軽量な形式である。このドキュメントでは、フィールド、配列、オブジェクトなど、JSON 標準で定義された多くの用語を使用する。
* GeoJSON - [GeoJSON](https://geojson.org/) は、さまざまな地理データ構造を符号化するための形式である。

<a id="presence"></a>
### 必須性

フィールドおよびファイルに適用される必須性の区分は次のとおり。

* 必須（REQUIRED） - ファイルまたはフィールドはデータセットに含めなければならず（MUST）、各レコードのフィールドには値を指定しなければならない（MUST）。
* 任意（OPTIONAL） - ファイルまたはフィールドはデータセットから省略してもよく（MAY）、どのレコードでもフィールドの値を省略してもよい（MAY）。
* 条件付きで必須（Conditionally REQUIRED） - ファイルまたはフィールドは、ファイルまたはフィールドの説明に記載された特定の条件の下で必須（REQUIRED）となる。それらの条件以外では、ファイルまたはフィールドは任意（OPTIONAL）である。

> 訳注: 本文中のフィールドの説明では、この一覧に無い「禁止（FORBIDDEN）」も使われている。GTFS と同様に「その条件ではファイルまたはフィールドを含めてはならない」という意味と解される。

<a id="field-types"></a>
### フィールドの型

- **Array** - 0 個以上の値の順序付きの並びからなる JSON 要素。
- **Color** - 6 桁の 16 進数で符号化された色。有効な値の生成には [https://htmlcolorcodes.com](https://htmlcolorcodes.com) を参照（先頭の「#」は含めない）。 <br> *例: 白は `FFFFFF`、黒は `000000`。*
- **Date** - YYYYMMDD 形式の運行日。運行日の中の時刻は 24:00:00 を超えることがあるため、1 つの運行日に翌日（以降）の情報が含まれることがある。 <br> *例: 2021 年 11 月 9 日は `20211109`。*
- **Email** - メールアドレス。 <br> *例: `example@example.com`*
- **Enum** - 「説明」列に列挙された、あらかじめ定義された定数の集合から選ぶ選択肢。 <br> *例: `wheelchair_boarding` フィールドを指定する場合、`boarding_accessible`、`boarding_inacessible`、またはリストにあるその他の選択肢のいずれかを示さなければならない（MUST）。*
- **GeoJSON FeatureCollection** - [IETF RFC 7946-3.3](https://tools.ietf.org/html/rfc7946#section-3.3) に記述された FeatureCollection。
- **GeoJSON Polygon** - [IETF RFC 7946-3.1.6](https://tools.ietf.org/html/rfc7946#section-3.1.6) に記述された Geometry オブジェクト。
- **ID** - その特定のエンティティを識別する文字列として表す。ID は次の条件を満たす。
    * 同種のフィールドの中で一意でなければならない（MUST）（例: `id` はゾーンの間で一意でなければならない（MUST））
    * 特に指定のない限り、グローバルに一意である必要はない
    * スペースを含んではならない（MUST NOT）
    * 特定のエンティティ（ゾーン、プランなど）に対して永続的でなければならない（MUST）。
- **Language** - IETF BCP 47 の言語コード。IETF BCP 47 の概要については [http://www.rfc-editor.org/rfc/bcp/bcp47.txt](http://www.rfc-editor.org/rfc/bcp/bcp47.txt) および [http://www.w3.org/International/articles/language-tags/](http://www.w3.org/International/articles/language-tags/) を参照。 <br> *例: 英語は `en`、アメリカ英語は `en-US`、ドイツ語は `de`。*
- **Non-negative Integer** - 0 以上の整数。
- **Float** - 浮動小数点数。
- **Object** - キーと値の組（フィールド）からなる JSON 要素。
- **Phone number** - 電話番号。電話番号には国番号を含めなければならない（MUST）。電話番号には区切り記号や、ダイヤル用の文字表記を含めてはならない（MUST NOT）。 <br> *例: 北米の電話番号「(987) 654-3210」は `+19876543210` として、フランスの電話番号「01.23.45.67.89」は `+33123456789` として指定しなければならない（MUST）*。（訳注: 日本の電話番号「03-1234-5678」は `+81312345678` となる。）
- **String** - 表示を目的とし、それゆえ人が読めるものでなければならない、UTF-8 文字のテキスト文字列。
- **Time** - HH:MM:SS 形式の時刻（H:MM:SS も可）。時刻は運行日の「正午マイナス 12 時間」から計測する（夏時間の切り替えが発生する日を除けば、実質的には午前 0 時）。午前 0 時を過ぎて発生する時刻は、その運行スケジュールが始まる日の現地時刻で、24:00:00 より大きい HH:MM:SS の値として入力する。 <br> *例: 午後 2 時 30 分は `14:30:00`、翌日の午前 1 時 35 分は `25:35:00`。*
- **Timezone** - [https://www.iana.org/time-zones](https://www.iana.org/time-zones) の TZ タイムゾーン。タイムゾーン名にスペース文字は含まれないが、アンダースコアは含まれることがある。有効な値の一覧は [http://en.wikipedia.org/wiki/List\_of\_tz\_zones](http://en.wikipedia.org/wiki/List\_of\_tz\_zones) を参照。 <br> *例: `Asia/Tokyo`、`America/Los_Angeles`、`Africa/Cairo`。*
- **URL** - http:// または https:// を含む完全修飾 URL。URL 内の特殊文字は正しくエスケープされていなければならない。完全修飾 URL の値の作成方法については [http://www.w3.org/Addressing/URL/4\_URI\_Recommentations.html](http://www.w3.org/Addressing/URL/4\_URI\_Recommentations.html) を参照。
- **Currency code** - ISO 4217 で定義された 3 文字の通貨コードを含む文字列。例: "CAD"、"USD"。（訳注: 日本円は "JPY"。）
* **Latitude** - 10 進数の度で表した WGS84 の緯度。値は -90.0 以上 90.0 以下でなければならない（MUST）。例: ローマのコロッセオは `41.890169`。
* **Longitude** - 10 進数の度で表した WGS84 の経度。値は -180.0 以上 180.0 以下でなければならない（MUST）。例: ローマのコロッセオは `12.492269`。
- **Timestamp** - 1970 年 1 月 1 日 00:00:00 UTC（Unix エポック）からの経過秒数を表す整数。

<a id="dataset-files"></a>
## データセットのファイル

デフォルトでは、オンデマンドサービスはどこでも利用できない。運行中のオンデマンドサービスを表すには、`zones.json` と `operating_rules.json` に、それぞれ少なくとも 1 つのゾーンと 1 つの運行ルールを定義しなければならない（MUST）。

ファイル名 | 必須性 | 説明
---|---|---
`gofs.json` | 必須 | オンデマンドサービスシステムのデータ提供者が公開する、他のすべてのファイルへのリンクを持つ自動検出ファイル。
`gofs_versions.json` | 任意 | 同じ GOFS フィードで利用可能な各バージョンを示す。
`system_information.json` | 必須 | オンデマンドサービスシステムの属性（運行事業者、所在地、導入年、URL、連絡先、タイムゾーンなど）を定義する。
`service_brands.json` | 必須 | 乗客が利用できるさまざまなオンデマンドサービスブランドの詳細を示す。
`vehicle_types.json` | 条件付きで必須 | オンデマンドサービスの運行に使用される車両タイプを記述する。`operating_rules.json` でいずれかの車両タイプが参照されている場合、このファイルは必須（REQUIRED）である。
`zones.json` | 必須 | 乗客がオンデマンドサービスを利用できるゾーンを地理的に定義する。
`operating_rules.json` | 必須 | ゾーン内移動およびゾーン間移動のルールと、運行時間を定義する。
`calendars.json` | 必須 | 乗客がオンデマンドサービスを利用できる日付と曜日を定義する。
`fares.json` | 任意 | システムの静的な運賃ルールを定義する。
`wait_time` | 条件付きで必須 | 問い合わせた地域の待ち時間を返す。`booking_rules` が無い場合、または少なくとも 1 つの `booking_rule` が `booking_type=real-time` である場合は、`wait_time` か `realtime_booking` のいずれかを提供しなければならない（MUST）。
`booking_rules.json` | 任意 | 問い合わせた地域における予約のルールを返す。
`realtime_booking` | 任意 | 静的な予約情報を提供できない場合に、利用可能な予約の詳細を返す。`booking_rules` が無い場合、または少なくとも 1 つの `booking_rule` が `booking_type=real-time` である場合は、`wait_time` か `realtime_booking` のいずれかを提供しなければならない（MUST）。

> 訳注: `booking_type` は [booking_rules.json](#booking_rulesjson) で数値の列挙値（`0`, `1`, `2`）として定義されている。`booking_type=real-time` は `booking_type=0`（リアルタイム予約）を指すと解される。

<a id="file-requirements"></a>
## ファイルの要件

<a id="auto-discovery"></a>
### 自動検出

データ提供者は、`gofs.json` 自動検出エンドポイントの場所へのリンクを置くことで、GOFS フィードの自動検出を実装すべきである（SHOULD）。

* 自動検出ファイルの場所は、`system_information.json` ファイルの URL フィールドで指定された URL にある、オンデマンドサービスのランディングページの HTML 内で提供すべきである（SHOULD）。
* これは次の形式の _link_ タグで参照する。
  * `<link rel="gofs" type="application/json" href="https://www.example.com/data/gofs.json" />`
  * 参考:
    * https://microformats.org/wiki/existing-rel-values
    * https://microformats.org/wiki/rel-faq#How_is_rel_used
  * オンデマンドサービスのランディングページには、複数のシステムの自動検出ファイルへのリンクを含めてもよい（MAY）。

<a id="versioning"></a>
### バージョン管理

データ利用アプリケーションとの後方互換性を損なうような変更も含めて GOFS を発展させられるよう、GOFS のドキュメントはバージョン管理されている。GOFS のバージョンは "vX.Y" と命名され、`X.Y` はバージョン番号である。

* 現在のリリースは v1.0 である。

<a id="localization"></a>
### ローカライズ

各データファイル群は、system_information.json で定義された単一の言語で配布すべきである（SHOULD）。複数の言語でフィードを公開したいシステムは、次のように複数の配布物を公開することで対応すべきである（SHOULD）。
* `https://www.example.com/data/en/system_information.json`
* `https://www.example.com/data/fr/system_information.json`

<a id="output-format"></a>
### 出力形式

本仕様に示すすべての JSON ファイルは、JSON レスポンスオブジェクトの最上位に、同じ共通ヘッダー情報を含む。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`last_updated` | 必須 | Timestamp | フィード内のデータが最後に更新された時刻を示す。このタイムスタンプは、この時点におけるシステムの現在の状態について、データ提供者が把握している内容を表す。
`ttl` | 必須 | Non-negative integer | フィード内のデータが次に更新されるまでの秒数。データを常に再取得すべき場合、値は `0` とすべきである（SHOULD）。
`version`  | 必須 | String | バージョン管理の枠組みに従った、フィードが準拠する GOFS のバージョン番号。
`data` | 必須 | Object | 名前:値の組の形式のレスポンスデータ。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 3600,
  "version": "1.0",
  "data": {
    "language": "en",
    "timezone": "US/Central",
    "name": "Example MicroTransit"
  }
}
```

<a id="field-definitions"></a>
## フィールドの定義

### gofs.json

`gofs.json` 検出ファイルは、車両が運行される単一のシステムまたは地理的エリアを表すべきである（SHOULD）。`gofs.json` ファイルの場所（URL）は、本仕様の[自動検出](#auto-discovery)機能を用いて一般に公開すべきである（SHOULD）。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`language` | 必須 | Language | 残りのファイル全体で使用される言語。[system_information.json](#system_informationjson) ファイルの値と一致しなければならない（MUST）。
\-&nbsp;`feeds` | 必須 | Array | この自動検出ファイルによって公開されるすべてのフィードの配列。配列の各要素は、以下のキーを持つオブジェクトである。
&emsp;\-&nbsp;`name` | 必須 | String | フィードの種類を識別するキー。キーは、対応するフィードの種類について本仕様で定義された基本ファイル名でなければならない（MUST）（`zones.json` ファイルなら `zones`、`operating_rules.json` ファイルなら `operating_rules`）。
&emsp;\-&nbsp;`url` | 必須 | URL | フィードの URL。実際のフィードのエンドポイント（URL）は `file_name.json` の形式で定義されていなくてもよい（MAY NOT）ことに注意。例えば、有効なフィードのエンドポイントは `zones.json` ではなく `zones` で終わってもよい。

> 訳注: 上の表では `language` と `feeds` が "data" オブジェクト直下に並ぶように読めるが、次の例では "data" の下が言語コード（`"en"`、`"fr"`）をキーとするオブジェクトになっており、`language` フィールドが無い。表と例の構造が一致していない。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 0,
  "version": "1.0",
  "data": {
    "en": {
      "feeds": [
        {
          "name": "system_information",
          "url": "https://www.example.com/gofs/1/en/system_information"
        },
        {
          "name": "zones",
          "url": "https://www.example.com/gofs/1/en/zones"
        }
      ]
    },
    "fr" : {
      "feeds": [
        {
          "name": "system_information",
          "url": "https://www.example.com/gofs/1/fr/system_information"
        },
        {
          "name": "zones",
          "url": "https://www.example.com/gofs/1/fr/zones"
        }
      ]
    }
  }
}
```
### gofs_versions.json

`gofs_versions.json` には、オンデマンドサービスシステムを表す同じ GOFS フィードについて、利用可能なすべてのバージョンを含めるべきである（SHOULD）。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性| 型 | 定義
---|---|---|---
`versions` | 必須 | Array | フィードの利用可能なバージョンごとに、以下で定義するオブジェクトを 1 つずつ含む。配列はバージョン番号の昇順に並べなければならない（MUST）。
\-&nbsp;`version` | 必須 | String | フィードのバージョン番号。
\-&nbsp;`url` | 必須 | URL | 対応する `gofs.json` エンドポイントの URL。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 0,
  "version": "1.0",
  "data": {
    "versions": [
      {
        "version": "1.0",
        "url": "https://www.example.com/gofs/2/gofs"
      },
      {
        "version": "X.Y",
        "url": "https://www.example.com/gofs/3/gofs"
      }
    ]
  }
}
```

### system_information.json

このファイルは、オンデマンドサービスシステムの属性を定義する。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`language` | 必須 | Language | 残りのファイル全体で使用される言語。
`timezone` | 必須 | Timezone | オンデマンドサービスシステムが所在するタイムゾーン。
`name` | 必須 | String | 乗客に表示する、オンデマンドサービスシステムの名称。
`short_name` | 任意 | String | オンデマンドサービスシステムの名称として一般に使われる略称。
`operator` | 任意 | String | オンデマンドサービスの運行事業者の名称。運行事業者名はシステム名と同じでもよい（MAY）。
`url` | 任意 | URL | オンデマンドサービスシステムの URL。
`subscribe_url` | 任意 | URL | 乗客がオンデマンドサービスに登録できる URL。
`start_date` | 任意 | Date | システムが運行を開始した日付。
`phone_number` | 任意 | Phone Number | 当該システムのカスタマーサービス部門の音声通話用電話番号。
`email` | 任意 | Email | 運行事業者のカスタマーサービス部門が常時確認している連絡用メールアドレス。このメールアドレスは、乗客がカスタマーサービス担当者に連絡できる直接の窓口であるべきである（SHOULD）。
`feed_contact_email` | 任意 | Email | データ利用者がフィードの技術的な問題を報告するための連絡用メールアドレス。


##### 例:

```jsonc
{
  "last_updated": 1611598155,
  "ttl": 1800,
  "version": "1.0",
  "data": {
    "language": "en",
    "timezone": "America/Toronto",
    "name": "Example MicroTransit",
    "short_name": "Micro",
    "operator": "MicroTransit, Inc",
    "url": "https://www.example.com",
    "subscribe_url": "https://www.example.com",
    "start_date": "20100610",
    "phone_number": "+18005551234",
    "email": "customerservice@example.com",
    "feed_contact_email": "datafeed@example.com"
  }
}
```

### service_brands.json

このファイルは、乗客が利用できるオンデマンドサービスブランドを定義する。1 つのフィードに、異なる特徴や設備を持つ複数のサービスブランドを含めてもよい（MAY）（例: 配車サービスのシステムが「Regular Ride」「Large Ride」「Shared Ride」のサービスを提供してもよい（MAY））。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`service_brands` | 必須 | Array | 以下で定義するサービスブランドごとに 1 つのオブジェクトを含む配列。
\-&nbsp;`brand_id` | 必須 | ID | サービスブランドの一意な識別子。この値は、サービスが提供されている期間を通じて同じままであるべきである（SHOULD）。
\-&nbsp;`brand_name` | 必須 | String | 乗客に表示する、サービスブランドの名称。
\-&nbsp;`brand_color` | 任意 | Color | 乗客に表示する、サービスブランドを識別する色
\-&nbsp;`brand_text_color` | 任意 | Color | `brand_color` の上にテキストを表示する際に使用する色。視覚的なアクセシビリティの観点から、`brand_text_color` は `brand_color` と十分なコントラストを持たなければならない（MUST）（例: 暗い `brand_color` には白の `brand_text_color` を組み合わせるべきであり（SHOULD）、明るい `brand_color` には黒の `brand_text_color` を組み合わせるべきである（SHOULD））。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 0,
  "version": "1.0",
  "data": {
    "service_brands": [
      {
        "brand_id": "regular_ride",
        "brand_name": "Regular Ride",
        "brand_color": "1C7F49",
        "brand_text_color": "FFFFFF"
      },
      {
        "brand_id": "large_ride",
        "brand_name": "Large Ride",
        "brand_color": "1C7F49",
        "brand_text_color": "FFFFFF"
      },
      {
        "brand_id": "shared_ride",
        "brand_name": "Shared Ride",
        "brand_color": "1C7F49",
        "brand_text_color": "FFFFFF"
      }
    ]
  }
}
```

### vehicle_types.json

このファイルは、オンデマンドサービスの運行に使用される車両タイプを定義する。`operating_rules.json` でいずれかの車両タイプが参照されている場合、このファイルは必須（REQUIRED）である。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`vehicle_types` | 必須 | Array | 以下で定義する車両タイプごとに 1 つのオブジェクトを含む配列。
\-&nbsp; `vehicle_type_id` | 必須 | ID | 車両タイプの一意な識別子。
\-&nbsp; `max_capacity` | 任意 | Non-Negative Integer | その車両が法的に乗せることのできる乗客の最大人数。
\-&nbsp; `wheelchair_boarding` | 任意 | Enum | 車いすを使用する乗客がその車両に乗車できるかどうか。有効な選択肢は次のとおり。<br /><ul><li>`boarding_accessible`</li><li>`boarding_inaccessible`</li><li>`boarding_accessible_with_assistance`</li></ul>

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 0,
  "version": "1.0",
  "data": {
    "vehicle_types": [
      {
        "vehicle_type_id": "large_van",
        "max_capacity": 7,
        "wheelchair_boarding": "boarding_accessible"
      }
    ]
  }
}
```

### zones.json

このファイルは、乗客がオンデマンドサービスを利用できるゾーンを地理的に定義する。ゾーンは、[RFC 7946](https://tools.ietf.org/html/rfc7946) に従った "FeatureCollection" の GeoJSON ファイルで区切られる。少なくとも 1 つのゾーンを定義しなければならない（MUST）。

このファイルで定義されるすべてのゾーンは公開情報である（つまり、すべてのゾーンは誰もが閲覧できる地図上に表示できる）。

位置の判定は 2 次元で行われる。高架道路や橋の上での乗車または降車が許可されている場合、その下の車道や通路でも許可される。GPS、携帯電話、Wi-Fi の信号による位置データは干渉を受けるため、その精度は数十メートル、またはそれ以上の誤差を伴う。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
 `zones` | 必須 | GeoJSON FeatureCollection | [RFC 7946](https://tools.ietf.org/html/rfc7946) に従ったオブジェクト。|
 -&nbsp;`type` | 必須 | String | [RFC 7946](https://tools.ietf.org/html/rfc7946) に従った `FeatureCollection`。 |
 -&nbsp;`features` | 必須 | Array | 各オブジェクトが 1 つのゾーンを表す、以下で定義するオブジェクトの配列。 |
 -&nbsp;\-&nbsp;`type` | 必須 | String | [RFC 7946](https://tools.ietf.org/html/rfc7946) に従った `Feature`。 |
 -&nbsp;\-&nbsp;`zone_id` | 必須 | ID | ゾーンの一意な識別子。 |
 -&nbsp;\-&nbsp;`geometry` | 必須 | GeoJSON Polygon | 乗客が乗車または降車できる場所を表すポリゴン。 <p> [右手の法則](https://tools.ietf.org/html/rfc7946#section-3.1.6)に従い、時計回りの点の並びはポリゴンで囲まれた領域、すなわち乗車と降車を行ってもよい（MAY）領域を定義する。一方、反時計回りの並びはポリゴンの外側の領域、すなわち乗車と降車を行うことができない（MAY NOT）領域を定義する。 |
 -&nbsp;\-&nbsp;`properties` | 必須 | Object | 位置のプロパティのキー。 |
 -&nbsp;\-&nbsp;\-&nbsp;`name` | 任意 | String | 乗客に表示するゾーンの名称を示す。 |

> 訳注: RFC 7946 §3.1.6 の右手の法則では、外周リングは反時計回り、穴（内側のリング）は時計回りとされており、上の `geometry` の説明とは向きが逆である。また、次の例でも外周リング（zoneA）は反時計回り、穴は時計回りになっており、RFC 7946 と一致している。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 0,
  "version": "1.0",
  "data": {
    "zones": {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "zone_id": "zoneA",
          "properties": {
            "name": "Montréal Area"
          },
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  -74.10,
                  45.35
                ],
                [
                  -73.30,
                  45.35
                ],
                [
                  -73.30,
                  45.75
                ],
                [
                  -74.10,
                  45.75
                ],
                [
                  -74.10,
                  45.35
                ]
              ],
              [
                [
                  -73.60,
                  45.55
                ],
                [
                  -73.60,
                  45.65
                ],
                [
                 -73.50,
                  45.65
                ],
                [
                  -73.50,
                  45.55
                ],
                [
                  -73.60,
                  45.55
                ]
              ]
            ]
          }
        }
      ]
    }
  }
}
```

### operating_rules.json

このファイルには、時間帯とカレンダーに従って、ゾーン間または同一ゾーン内でのオンデマンドサービスを可能にする運行ルールを記述する。少なくとも 1 つの運行ルールを定義しなければならない（MUST）。`start_pickup_window`、`end_pickup_window`、`end_dropoff_window` が指定されていない場合、オンデマンドサービスは 1 日のどの時間帯でも利用できるものとみなされる。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`operating_rules` | 必須 | Array | 以下で定義する運行ルールごとに 1 つのオブジェクトを含む配列。
\-&nbsp; `from_zone_id` | 必須 | ID | 当該ルールにおける乗車ゾーンを表す、`zones.json` で定義されたゾーンの ID。
\-&nbsp; `to_zone_id` | 必須 | ID | 当該ルールにおける降車ゾーンを表す、`zones.json` で定義されたゾーンの ID。`from_zone_id` と `to_zone_id` は同じゾーンを参照してもよい（MAY）。
\-&nbsp; `start_pickup_window` | 条件付きで必須 | Time | この配列で定義された `from_zone_id` で乗車が可能になる時刻。`start_pickup_window` を指定する場合、`end_pickup_window` か `end_dropoff_window` のいずれかも指定しなければならない（MUST）。
\-&nbsp; `end_pickup_window` | 条件付きで必須 | Time | この配列で定義された `from_zone_id` で乗車ができなくなる時刻。`end_pickup_window` を指定する場合、`start_pickup_window` を指定しなければならない（MUST）。
\-&nbsp; `end_dropoff_window` | 条件付きで必須 | Time | この配列で定義された `to_zone_id` で降車ができなくなる時刻。乗車可能時間の終了と降車可能時間の終了が異なるサービスもある（例: 出発ゾーンでの乗車は午後 10 時で終了するが、目的地ゾーンでは午後 10 時 30 分まで降車できる）。`end_dropoff_window` を指定する場合、`start_pickup_window` を指定しなければならない（MUST）。
\-&nbsp; `calendars` | 必須 | Array | 乗車と降車が行われる日付と曜日を定義する、`calendars.json` のカレンダー ID の配列。
\-&nbsp; `brand_id` | 任意 | ID | `service_brands.json` で定義されたサービスブランドの ID。このフィールドが指定されていない場合、運行ルールは `service_brands.json` で定義されたすべてのサービスブランドに適用される。
\-&nbsp; `vehicle_type_id` | 必須 | Array | オンデマンドサービスの提供に使用される車両タイプの配列。
\-&nbsp; `fare_id` | 任意 | ID | 運賃の一意な識別子。オンデマンドサービスの価格を決定するために使用する。

> 訳注: `vehicle_type_id` は必須とされているため、運行ルールは常に車両タイプを参照することになる。そうすると、[データセットのファイル](#dataset-files)で「条件付きで必須」とされている `vehicle_types.json` も、実質的には常に必須となる。


##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 0,
  "version": "1.0",
  "data": {
    "operating_rules" : [
      {
        "from_zone_id": "zoneA",
        "to_zone_id": "zoneA",
        "start_pickup_window" : "06:00:00",
        "end_pickup_window": "09:00:00",
        "end_dropoff_window": "09:30:00",
        "calendars": ["weekend", "labor_day"],
        "brand_id": "large_ride",
        "vehicle_type_id": ["large_van"],
        "fare_id": "RegularPrice"
      }
   ]
  }
}
```

### calendars.json

このファイルは、乗客がオンデマンドサービスを利用できる日付と曜日を定義する。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`calendars` | 必須 | Array | 以下で定義するカレンダーごとに 1 つのオブジェクトを含む配列。
\-&nbsp;`calendar_id` | 必須 | ID | カレンダーの一意な識別子。
\-&nbsp;`days` | 任意 | Array | このオブジェクトが適用される曜日の、英語名の略称（先頭 3 文字）の配列（例: `["mon", "tue", "wed", "thu", "fri", "sat, "sun"]`）。曜日が定義されていない場合、オンデマンドサービスはすべての曜日に利用できるものとみなされる。
\-&nbsp;`start_date` | 必須 | Date | カレンダーの開始日。
\-&nbsp;`end_date` | 必須 | Date | カレンダーの終了日。終了日は開始日と同じかそれ以降でなければならない（MUST）。
\-&nbsp;`excepted_dates` | 任意 | Array | カレンダーからサービスの提供を除外する日付の配列。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 86400,
  "version": "1.0",
  "data": {
    "calendars": [
      {
         "calendar_id": "weekday",
         "days": [
            "mon",
            "tue",
            "wed",
            "thu",
            "fri"
         ],
         "start_date": "20210901",
         "end_date": "20211031",
         "excepted_dates": [
            "20210906"
         ]
      },
      {
         "calendar_id": "weekend",
         "days": [
            "sat",
            "sun"
         ],
         "start_date": "20210901",
         "end_date": "20211031"
      },
      {
         "calendar_id": "labor_day",
         "start_date": "20210906",
         "end_date": "20210906"
      }
    ]
  }
}
```

### fares.json

このファイルは、システムの運賃の計算方法を定義する。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`fares` | 必須 | Array | 以下で定義する運賃定義ごとに 1 つのオブジェクトを含む配列。
\-&nbsp;`fare_id` | 必須 | ID | 運賃の一意な識別子。
\-&nbsp;`currency` | 必須 | Currency code | 運賃の通貨。
\-&nbsp;`kilometer` | 任意 | Array | 1 キロメートルあたりのサービス価格を定義する Fare オブジェクトの配列。乗客 1 人あたりの総額は、`rider` で定義された基本価格に、`kilometer`、`minute`、`active_minute`、`idle_minute` のすべての区分を加算したものである。
\-&nbsp;`minute` | 任意 | Array | 車両が動いているかどうかにかかわらず、1 分あたりのサービス価格を定義する Fare オブジェクトの配列。乗客 1 人あたりの総額は、`rider` で定義された基本価格に、`kilometer`、`minute`、`active_minute`、`idle_minute` の該当するすべての区分を加算したものである。
\-&nbsp;`active_minute` | 任意 | Array | 車両が走行している間の、1 分あたりのサービス価格を定義する Fare オブジェクトの配列。乗客 1 人あたりの総額は、`rider` で定義された基本価格に、`kilometer`、`minute`、`active_minute`、`idle_minute` の該当するすべての区分を加算したものである。
\-&nbsp;`idle_minute` | 任意 | Array | 車両が停止している、または動いていない間の、1 分あたりのサービス価格を定義する Fare オブジェクトの配列。乗客 1 人あたりの総額は、`rider` で定義された基本価格に、`kilometer`、`minute`、`active_minute`、`idle_minute` の該当するすべての区分を加算したものである。
\-&nbsp;`rider` | 任意 | Array | 乗客 1 人あたりの基本価格を定義する Fare オブジェクトの配列。
\-&nbsp;`luggage` | 任意 | Array | 荷物 1 個あたりの追加料金として、荷物の価格を定義する Fare オブジェクトの配列。

以下は "Fares" オブジェクトの構造である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`interval` | 任意 | Float | 親キーの単位で表した、この行の `amount` を開始（start）から終了（end）まで適用する間隔。
`start` | 任意 | Non-negative Integer | 親キーの単位で表した、このオブジェクトで定義された `amount` の課金が始まる値。
`end` | 任意 | Non-negative Integer | 親キーの単位で表した、このオブジェクトで定義された `amount` の課金が終わる値。
`amount` | 任意 | Non-negative currency amount | 親キーの 1 単位あたりの運賃額。

##### 例 1: 距離制運賃

最初の 10 キロメートルは 1 キロメートルあたり 3.30 CAD で、250 メートルごとに課金される。それ以降は 1 キロメートルあたり 4.30 CAD で、500 メートルごとに課金される。

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 86400,
  "version": "1.0",
  "data": {
    "fares": [
      {
        "fare_id": "RegularPrice",
        "currency": "CAD",
        "kilometer": [
          {
            "interval": 0.25,
            "end": 10,
            "amount": 3.30
          },
          {
            "interval": 0.5,
            "start": 10,
            "amount": 4.30
          }
        ]
      }
    ]
  }
}
```

##### 例 2: 時間制運賃

最初の 20 分は 1 分あたり $1.00 CAD で、1 分ごとに課金される。20 分を過ぎると、利用者は 1 分あたり $1.50 を 30 秒ごとに支払う。

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 86400,
  "version": "1.0",
  "data": {
    "fares": [
      {
        "fare_id": "RegularPrice",
        "currency": "CAD",
        "minute": [
          {
            "interval": 1,
            "end": 20,
            "amount": 1.0
          },
          {
            "interval": 0.5,
            "start": 20,
            "amount": 1.5
          }
        ]
      }
    ]
  }
}
```

##### 例 3: 組み合わせ価格

利用者は、最初の 10km については基本価格の $2.50 CAD を超えて支払うことはない。10km を超えると、利用者は 1km あたり $1.00 CAD を支払う。25km を超えると、利用者は $1.00/km に加えて、5km ごとに $3.00 CAD の延長価格を追加で支払う。利用者は荷物を 2 個まで無料で持ち込むことができ、それを超える荷物 1 個につき $5 が課金される。

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 86400,
  "version": "1.0",
  "data": {
    "fares": [
      {
        "fare_id": "RegularPrice",
        "currency": "CAD",
        "kilometer": [
          {
            "interval": 1.0,
            "start": 10,
            "amount": 1.0
          },
          {
            "interval": 5,
            "start": 25,
            "amount": 3.0
          }
        ],
        "rider": [
          {
            "amount": 2.5
          }
        ],
        "luggage": [
          {
            "start": 3,
            "amount": 5
          }
        ]
      }
    ]
  }
}
```

### wait_time

この動的クエリは、特定の地点における待ち時間を返す。`wait_time` リクエストは、利用者の操作のたびに行わなければならない。

リクエストには、次のクエリパラメータを含めなければならない。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`pickup_lat` | 必須 | Latitude | 利用者が乗車する地点の緯度。
`pickup_lon` | 必須 | Longitude | 利用者が乗車する地点の経度。
`drop_off_lat` | 条件付きで必須 | Latitude | 利用者が降車する地点の緯度。`drop_off_lon` を指定する場合は必須。それ以外の場合は禁止（FORBIDDEN）。
`drop_off_lon` | 条件付きで必須 | Longitude | 利用者が降車する地点の経度。`drop_off_lat` を指定する場合は必須。それ以外の場合は禁止（FORBIDDEN）。
`brand_id` | 条件付きで必須 | ID |  Array | `service_brands.json` で定義されたサービスブランドの ID の配列。複数のサービスブランドが利用可能な場合は必須（REQUIRED）。

以下のフィールドはすべて、このクエリのレスポンスのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`wait_times` | 必須 | Array | `brand_id` ごとに 1 つのオブジェクトを含む配列。リクエストされた地点で待ち時間が得られない場合は空にすべきである。
\-&nbsp; `brand_id` | 必須 | ID | `service_brands.json` で定義されたサービスブランドの ID
\-&nbsp; `wait_time` | 必須 | Non-negative Integer | 乗車までに乗客がその地点で待つ必要がある待ち時間（秒）。

##### 例:

###### クエリ:

`https://www.example.com/gofs/1/en/wait_time?pickup_lat=45.60&pickup_lon=-73.30&brand_id=regular_ride,large_ride`

###### レスポンス:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 86400,
  "version": "1.0",
  "data": {
    "wait_times": [
      {
        "brand_id": "regular_ride",
        "wait_time": 300
      },
      {
        "brand_id": "large_ride",
        "wait_time": 600
      }
    ]
  }
}
```

### booking_rules.json

このファイルは、乗車の予約方法に関するルールを定義する。利用可能な場合、利用者は、リアルタイムに、事前通知のうえ当日分を、または後日分を予約できる。

以下のフィールドはすべて、このフィードのメインの "data" オブジェクト内の属性である。


| フィールド名 | 必須性 | 型 |説明 |
 ---------- | ---- | -------- | ----------- |
 `booking_rules` |  必須  | Array | 以下で定義する予約ルールごとに 1 つのオブジェクトを含む配列。 |
\-&nbsp;`from_zone_ids` | 必須 | Array | 待ち時間の更新対象エリアをカバーする、`zones.json` で定義されたゾーンの 1 つ以上の ID。
\-&nbsp;`to_zone_ids` | 任意 | Array | 目的地のエリアをカバーする、`zones.json` で定義されたゾーンの 1 つ以上の ID。
 \-&nbsp; `booking_type` | 必須 | Enum | どれだけ前もって予約できるかを示す。 <br><br>有効な選択肢は次のとおり。<br>`0` - リアルタイム予約。`wait_time` と組み合わせて使用する。 <br>`1` - 事前通知による当日予約まで。<br>`2` - 前日（以前）の予約まで。 ||
 \-&nbsp; `prior_notice_duration_min` | 条件付きで必須 | Integer | 移動の何分前までに予約リクエストを行う必要があるかを示す、最小の分数。`booking_type=1` の場合は必須（REQUIRED）。それ以外の場合は禁止（FORBIDDEN）。 |
 \-&nbsp; `prior_notice_duration_max` | 任意 | Integer | 移動の何分前から予約リクエストを行えるかを示す、最大の分数。`booking_type=1` の場合は任意（OPTIONAL）。それ以外の場合は禁止（FORBIDDEN）。|
 \-&nbsp; `prior_notice_last_day` | 条件付きで必須 | Integer | 予約リクエストを行える、移動の前の最終日（例: 「乗車の 1 日前の午後 5 時までに予約が必要」は `prior_notice_last_day=1` と表現する）。`booking_type=2` の場合は必須（REQUIRED）。それ以外の場合は禁止（FORBIDDEN）。|
 \-&nbsp; `prior_notice_last_time` | 条件付きで必須 | Time | 予約リクエストを行える、移動の前の最終日における最終時刻（例: 「乗車の 1 日前の午後 5 時までに予約が必要」は `prior_notice_last_time=17:00:00` と表現する）。`prior_notice_last_day` が定義されている場合は必須（REQUIRED）。それ以外の場合は禁止（FORBIDDEN）。 |
 \-&nbsp; `prior_notice_start_day` | 任意 | Integer | 予約リクエストを行える、移動の前の最も早い日（例: 「最も早くて 1 週間前の午前 0 時から予約可能」は `prior_notice_start_day=7` と表現する）。`booking_type=0` の場合は禁止（FORBIDDEN）。`booking_type=1` で `prior_notice_duration_max` が定義されている場合は禁止（FORBIDDEN）。それ以外の場合は任意（OPTIONAL）。 |
 \-&nbsp; `prior_notice_start_time` | 条件付きで必須 | Time | 予約リクエストを行える、移動の前の最も早い日における最も早い時刻（例: 「最も早くて 1 週間前の午前 0 時から予約可能」は `prior_notice_start_time=00:00:00` と表現する）。`booking_type=0` の場合は禁止（FORBIDDEN）。`prior_notice_start_day` が定義されている場合は必須（REQUIRED）。それ以外の場合は禁止（FORBIDDEN）。 |
 \-&nbsp; `prior_notice_calendar_id` | 任意 | `calendars.json` の `calendar_id` を参照する ID | `prior_notice_last_day` や `prior_notice_start_day` を数える対象となる運行日を示す（例: 空の場合、`prior_notice_start_day=2` は暦日で 2 日前となる。営業日（祝日を除く平日）のみを含む `calendar_id` として定義されている場合、`prior_notice_start_day=2` は 2 営業日前となる）。`booking_type=2` の場合は任意（OPTIONAL）。それ以外の場合は禁止（FORBIDDEN）。 |
 \-&nbsp; `message` | 任意 | String | ゾーン内でサービスを利用する乗客に、オンデマンドの乗車・降車を予約する際に表示するメッセージ。サービスを利用するために乗客が取るべき行動について、ユーザーインターフェース上で伝える最小限の情報を提供することを目的とする。 |
 \-&nbsp; `pickup_message` | 任意| String  | `message` と同様に機能するが、乗客がオンデマンドの乗車のみを利用する場合に使用する。 |
 \-&nbsp; `drop_off_message` | 任意| String | `message` と同様に機能するが、乗客がオンデマンドの降車のみを利用する場合に使用する。 |
 \-&nbsp; `phone_number` | 任意| Phone number | 予約リクエストを行うために電話をかける電話番号。 |
 \-&nbsp; `info_url` | 任意| URL | 予約ルールに関する情報を提供する URL。 |
 \-&nbsp; `booking_url` | 任意| URL  | 予約リクエストを行えるオンラインのインターフェースまたはアプリへの URL。 |

> 訳注: 次の例は JSON として正しくない（末尾の閉じ括弧 `}` が 1 つ多い）。また 2 つ目のルールは `booking_type=2` だが、上の表で必須とされている `prior_notice_last_day` が無く、`prior_notice_start_day` を指定しているのに必須の `prior_notice_start_time` も無い。

##### 例:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 86400,
  "version": "1.0",
  "data": {
    "booking_rules": [
        {
          "from_zone_ids": ["zoneA"],
          "to_zone_ids": null,
          "booking_type": 1,
          "prior_notice_duration_min": 30,
          "prior_notice_duration_max": 180
        },
        {
          "from_zone_ids": ["zoneA"],
          "to_zone_ids": ["zoneB"],
          "booking_type": 2,
          "prior_notice_start_day": 2,
          "prior_notice_last_time": "17:00:00"
        }
      ]
    }
  }
}
```

### realtime_booking
この動的クエリは、特定の地点について、時間・価格の見積もりと realtime_booking の情報を提供する。他のエンドポイントから得られる情報と比べて、特定の移動についてより細かい、またはより正確な予約情報を提供者が持てると見込まれる場合に使用できる。

例えば、提供者は、`fares.json` から得られる大まかなルールベースの価格情報と比べて、特定の移動についてより正確な価格情報を提供できる場合がある。

リクエストには、`wait_time` と同じクエリパラメータを含めなければならない。さらに、逆ジオコーディングの際に乗車地と降車地の住所が失われないよう、次の 2 つの任意のパラメータを指定できる。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`pickup_address` | 任意 | String | 利用者が乗車する地点の完全な住所。
`drop_off_address` | 任意 | String | 利用者が降車する地点の完全な住所。

以下のフィールドはすべて、このクエリのレスポンスのメインの "data" オブジェクト内の属性である。

フィールド名 | 必須性 | 型 | 説明
---|---|---|---
`realtime_booking` | 必須 | Array | `brand_id` ごとに 1 つのオブジェクトを含む配列。リクエストされた地点でリアルタイム予約が利用できない場合は空にすべきである。
\-&nbsp; `brand_id` | 必須 | ID | `service_brands.json` で定義されたサービスブランドの ID
\-&nbsp; `wait_time` | 必須 | Non-negative Integer | 乗車までに乗客がその地点で待つ必要がある待ち時間（秒）。
\-&nbsp; `travel_time` | 任意 | Non-negative Integer | 乗車地から降車地までの推定所要時間（秒）。降車地が指定されていない場合は提供できない。
\-&nbsp; `travel_cost` | 任意 | Non-negative currency amount | 乗車地から降車地までの移動の推定運賃額。降車地が指定されていない場合は提供できない。
\-&nbsp; `travel_cost_currency` | 条件付きで必須 | Currency code | `estimated_travel_cost` の通貨。`estimated_travel_cost` が指定されている場合は必須（REQUIRED）。
\-&nbsp; `booking_detail` | 任意 | Object | 任意で、リアルタイムの予約の詳細を含むオブジェクトを提供できる。
-&nbsp;\-&nbsp; `service_name` | 任意 | String | リアルタイムの予約状況の変化によってサービス名を変える必要がある場合、`service_name` を指定して、乗客に表示するオンデマンドサービスシステムの名称を更新できる。
-&nbsp;\-&nbsp; `android_uri` | 条件付きで必須 | URL | Android で予約アプリを開くことができる Android App Links。`android_uri`、`ios_uri`、`web_uri`、`phone_number` の少なくとも 1 つを提供する必要がある。
-&nbsp;\-&nbsp; `ios_uri` | 条件付きで必須 | URL | iOS で予約アプリを開くことができる iOS Universal Links。`android_uri`、`ios_uri`、`web_uri`、`phone_number` の少なくとも 1 つを提供する必要がある。
-&nbsp;\-&nbsp; `web_uri` | 条件付きで必須 | URL | 予約リクエストを行うためにアクセスする Web の URL。`android_uri`、`ios_uri`、`web_uri`、`phone_number` の少なくとも 1 つを提供する必要がある。
-&nbsp;\-&nbsp; `phone_number` | 条件付きで必須 | Phone Number | 予約リクエストを行うために電話をかける電話番号。`android_uri`、`ios_uri`、`web_uri`、`phone_number` の少なくとも 1 つを提供する必要がある。

> 訳注: `estimated_travel_cost` というフィールドは定義されておらず、`travel_cost` を指すと解される。

##### 例:

###### クエリ:

`https://www.example.com/gofs/1/en/realtime_booking?pickup_lat=45.60&pickup_lon=-73.30&brand_id=regular_ride,large_ride`

###### レスポンス:

```jsonc
{
  "last_updated": 1609866247,
  "ttl": 300,
  "version": "1.0",
  "data": {
    "realtime_booking": [
      {
        "brand_id": "regular_ride",
        "wait_time": 300,
        "travel_time": 300,
        "travel_cost": 30,
        "travel_cost_currency": "CAD",
        "booking_detail": {
            "service_name": "Taxi",
            "android_uri": "https://www.example.com/app?service_type=REG&platform=android",
            "ios_uri": "https://www.example.com/app?service_type=REG&platform=ios",
            "web_uri": "https://www.example.com/app?service_type=REG",
            "phone_number": "+18005551234"
        }
      },
      {
        "brand_id": "large_ride",
        "wait_time": 450,
        "travel_time": 300,
        "travel_cost": 45,
        "travel_cost_currency": "CAD",
        "booking_detail": {
            "service_name": "Taxi Van",
            "android_uri": "https://www.example.com/app?service_type=XL&platform=android",
            "ios_uri": "https://www.example.com/app?service_type=XL&platform=ios",
            "web_uri": "https://www.example.com/app?service_type=XL",
            "phone_number": "+18005551234"
        }
      }
    ]
  }
}
```


<a id="deeplink-with-query-params"></a>
### クエリパラメータ付きのディープリンク

`realtime_booking` で提供される URI（`android_uri`、`ios_uri`、`web_uri`）および `booking_rules` で提供される URI（`booking_url`）は、決められた一連のクエリパラメータに対応すべきである。

パラメータ | 必須性 | 型 | 説明
---|---|---|---
`pickup_lat` | 必須 | Latitude | 利用者が乗車する地点の緯度。
`pickup_lon` | 必須 | Longitude | 利用者が乗車する地点の経度。
`pickup_address` | 任意 | String | 利用者が乗車する地点の完全な住所。
`drop_off_lat` | 必須 | Latitude | 利用者が降車する地点の緯度。
`drop_off_lon` | 必須 | Longitude | 利用者が降車する地点の経度。
`drop_off_address` | 任意 | String | 利用者が降車する地点の完全な住所。
`pickup_time` | 任意 | Timestamp | 利用者が乗車する時刻を、Unix エポックからの秒数で示す。
`drop_off_time` | 任意 | Timestamp | 利用者が降車する時刻を、Unix エポックからの秒数で示す。

> 訳注: 次の例では、パラメータ名が表の `pickup_time` ではなく `pick_up_time` になっており、時刻の値（`1726173300000`）も秒ではなくミリ秒になっている。

#### 例

```
https://www.example.com?pickup_lat=45.52585187926036&pickup_lon=-73.59502716927499&drop_off_lat=45.53614412053443&drop_off_lon=-73.5130921428607&pick_up_time=1726173300000&drop_off_time=1726173600000
```

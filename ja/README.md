> [!NOTE]
> これは [GOFS](https://github.com/MobilityData/gofs) の `README.md` の**非公式**日本語訳である。MobilityData による公式の翻訳ではなく、仕様の正本は原文である。
> - 原文: https://github.com/MobilityData/gofs/blob/bd0f124eb6f0a81cdae6c19033039fd26d70fca4/README.md
> - 翻訳日: 2026-10-27（初稿）
> - 原文は [Apache License 2.0](../LICENSE) で公開されており、本訳はその翻訳（改変）である
> - 訳語と翻訳時の判断は [notes/](../notes/) を参照

<a id="gofs"></a>
# GOFS

（本プロジェクトは以前 GOFS-lite という名称だった。[MobilityData への移管について詳しくはこちら](https://mobilitydata.org/gofs-a-new-chapter-for-on-demand-transportation-data/)。）

General On-Demand Feed Specification（GOFS）は、オンデマンドサービスの提供者が自らのサービスを軽量な形式で定義し、交通アプリケーションが相互運用可能な方法でそれを利用できるようにするものである。

GOFS は、純粋なオンデマンド交通サービスが自らの提供内容に関する情報を提供するための軽量な形式を定義する。これは、公共交通のために General Transit Feed Specification（GTFS）があり、シェアサイクル、電動キックボードのシェアリング、カーシェア、その他の乗り捨て型（フリーフローティング）のセルフサービス型の移動手段のために General Bikeshare Feed Specification（GBFS）があるのと同様である。GOFS は、文脈が許す限り、[GTFS](https://github.com/google/transit/) および [GBFS](https://github.com/MobilityData/gbfs) とできるだけ多くの共通点を持つことを目指している。

GOFS は現在、次のようなオンデマンドサービスに対応している。
- 固定の経路を持たない
- ゾーンからゾーンへ運行される
- 誰でも利用できる
- リアルタイムに配車依頼できる

対応するサービスの例には、配車サービス（タクシーや Uber など）、オンデマンドのマイクロトランジット（[Metro Micro](https://micro.metro.net) や [のるーと](https://knowroute.jp/) など）、パラトランジット（訳注: 主に障害などにより路線バスや鉄道の利用が難しい人を対象とした、予約制の送迎サービス。日本の福祉有償運送や福祉タクシーなどの STS（スペシャル・トランスポート・サービス）に近い）がある。

対応していないサービスは、スケジュールが定められた固定型またはフレキシブル型の公共交通サービスである（それらのユースケースには GTFS および GTFS-Flex が対応している）。

将来の GOFS の拡張では、次のようなオンデマンドサービスに対応する可能性がある。
- カーブ・トゥ・カーブ（curb-to-curb）、停留所間（stop-to-stop）、ドア・トゥ・ドア（door-to-door）で運行される  
(訳注：curbは縁石、路肩。利用者の指定する場所の路肩で乗降する方式)
- 専有の乗車および／または相乗りの乗車を提供する
- 事前に予約できる

GOFS は作成途中であり、正確な価格設定や所要時間の推定など、重要な機能が現時点では欠けている。質問やコメントは [gofs@mobilitydata.org](mailto:gofs@mobilitydata.org) に送ることができる。

<a id="gofs-json-schema"></a>
## GOFS JSON スキーマ
GOFS フィードの検証に使用できる JSON スキーマは[こちら](https://github.com/MobilityData/gofs/tree/main/schema)にある。

<a id="gtfs-flex-to-gofs-converter"></a>
## GTFS-Flex から GOFS への変換ツール
[GTFS-Flex](https://gtfs.org/documentation/schedule/examples/flex/)（General Transit Feed Specification - Flexible services）のデータを [GOFS](https://github.com/MobilityData/GOFS/blob/main/reference.md)（General On-demand Feed Specification）形式に変換する [Python ツール](https://pypi.org/project/GTFS-flex-to-GOFS/)。[Transit](https://github.com/TransitApp) が開発・保守している。

<a id="community"></a>
## コミュニティ
GOFS はオープンな標準である。アイデアや技術の具体的な改善を提案し、技術的なサポートを互いに提供する、あなたのような利用者によって成り立っている。ぜひ参加してほしい。
- 公式の仕様変更プロセスは [governance.md](https://github.com/MobilityData/GOFS/blob/main/governance.md) にある。
- GOFS を改善するための成熟したアイデアは、[GitHub Issue](https://github.com/MobilityData/GOFS/issues/new) または Pull Request で提案できる。
- より大きな視点でのプロダクトやビジョンについての議論は、[GitHub Discussions](https://github.com/MobilityData/GOFS/discussions) で続けられている。
- その他の Q&A や利用者同士の技術サポートには、[MobilityData Slack の #GOFS](https://mobilitydata-io.slack.com/archives/C08TGF1HM9Q) を利用できる（[MobilityData Slack の初回登録](https://share.mobilitydata.org/slack)）。

<a id="gofs-use"></a>
## GOFS の利用事例

[GitHub Issue](https://github.com/MobilityData/GOFS/issues/new) で追加を提案し、既知の GOFS 導入事例の一覧づくりに協力してほしい。

**データを利用するアプリケーション（データ利用者）**
- [Transit app](https://blog.transitapp.com/gofs/)

**GOFS に対応しているベンダーおよびツール**
- [Demand Trans](https://demandtrans.com/)
- [Ecolane](https://www.ecolane.com/)
- [Freebee](https://ridefreebee.com/)
- [Pantonium](https://pantonium.com/)

**データセット**
- [systems.csv](https://github.com/MobilityData/GOFS/blob/main/systems.csv) を参照

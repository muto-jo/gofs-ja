# サンプル

公開情報をもとに作成した GOFS フィードのサンプルです。各サービス事業者の公式フィードではありません。

サービスごとにフォルダを分け、GOFS の各ファイルを置きます。

```
sample/
└── <サービス名>/
    ├── gofs.json
    ├── system_information.json
    ├── service_brands.json
    ├── zones.json
    ├── operating_rules.json
    ├── calendars.json
    └── ...
```

| フォルダ | 内容 |
|---|---|
| [go_kitatama/](go_kitatama/) | タクシー配車アプリ「GO」の北多摩交通圏（普通車・今すぐ呼ぶ） |

作成時の仕様の解釈や判断は [notes/implementation-notes.md](../notes/implementation-notes.md) にまとめています。

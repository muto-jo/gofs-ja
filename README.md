# GOFS 日本語訳（非公式）

[GOFS（General On-Demand Feed Specification）](https://github.com/MobilityData/gofs) の非公式日本語訳と、日本のオンデマンド交通サービスをもとにしたデータサンプルです。
日本の公共交通・オープンデータに関わる方が GOFS を知り、試すための参考資料として公開しています。

> [!NOTE]
> - 本リポジトリは MobilityData による公式の翻訳ではありません。仕様の正本は [原文](https://github.com/MobilityData/gofs) です
> - サンプルは公開情報をもとに作成したもので、各サービス事業者が提供する公式のフィードではありません

## 内容

| パス | 内容 |
|---|---|
| [ja/README.md](ja/README.md) | GOFS 概要（README.md の日本語訳） |
| [ja/reference.md](ja/reference.md) | 仕様リファレンス（reference.md の日本語訳） |
| [sample/](sample/) | データサンプル |
| [notes/](notes/) | 翻訳・サンプル作成時の検討メモ、訳語集 |
| [tools/](tools/) | サンプルの検証スクリプト |

## 現状と今後の予定

2026-10-28 時点の状況です。

**現状**

- [x] README.md・reference.md の日本語訳（初稿）
- [x] 翻訳時の判断の記録と訳語集（[notes/translation-notes.md](notes/translation-notes.md)、[notes/glossary.md](notes/glossary.md)）
- [x] 原文の誤りや食い違いの洗い出し（translation-notes.md の「リファレンス誤り」タグ、現在 9 件）

**今後の予定**

- [ ] 訳文の原文との照合・修正
- [ ] タクシー配車アプリ「GO」の公開情報をもとにしたサンプルフィードの作成（[sample/](sample/)）
  - GOFS の各ファイルの JSON テンプレート
  - 提供エリアのポリゴン（`zones.json`）
  - 作成時の仕様の解釈や判断の記録（[notes/implementation-notes.md](notes/implementation-notes.md)）
- [ ] 原文の誤りを MobilityData に報告（GitHub Issue）

## 翻訳元

- リポジトリ: https://github.com/MobilityData/gofs
- コミット: [`bd0f124eb6f0a81cdae6c19033039fd26d70fca4`](https://github.com/MobilityData/gofs/tree/bd0f124eb6f0a81cdae6c19033039fd26d70fca4)（2026-09-30）

原文と照らし合わせる場合や、サンプルを検証する場合は、このコミットの原文を `upstream/gofs` に取得してください（`upstream/` は本リポジトリには含めていません）。

```bash
git clone https://github.com/MobilityData/gofs.git upstream/gofs
git -C upstream/gofs checkout bd0f124eb6f0a81cdae6c19033039fd26d70fca4
```

## サンプルの検証

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/validate.py sample/<サービス名>
```

上で取得した原文の [JSON スキーマ](https://github.com/MobilityData/gofs/tree/bd0f124eb6f0a81cdae6c19033039fd26d70fca4/schema)（`upstream/gofs/schema/`。一部のファイルのみ・作成途中）で検証します。

## ライセンス

翻訳元の GOFS は [Apache License 2.0](LICENSE) で公開されており、本リポジトリの翻訳も同ライセンスに従います（翻訳は原文の改変にあたります）。

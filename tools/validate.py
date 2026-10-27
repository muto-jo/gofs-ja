"""GOFS サンプルフィードを原文リポジトリの JSON スキーマで検証する。

使い方: .venv/bin/python tools/validate.py sample/<サービス名>

- upstream/gofs/schema/ にスキーマがあるファイルはスキーマで検証する
- スキーマが無いファイル（fares.json など）は JSON として読めるかだけ確認する
- zones.json はジオメトリが有効か（自己交差などが無いか）を shapely で確認する
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "upstream" / "gofs" / "schema"


def validate_schema(path: Path, data: dict) -> list[str]:
    schema_path = SCHEMA_DIR / path.name
    if not schema_path.exists():
        return []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft7Validator(schema)
    return [
        f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}"
        for e in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    ]


def validate_zones(data: dict) -> tuple[list[str], list[str]]:
    """zones.json のジオメトリを確認し、(エラー, 情報) を返す。

    reference.md は「時計回り = 乗降できる範囲」としており、RFC 7946 の推奨
    （外周は反時計回り）と逆になっている。どちらが正しいかは未決なので
    （notes/translation-notes.md T-003）、外周の向きはエラーにせず情報として出す。
    """
    errors, infos = [], []
    features = data.get("data", {}).get("zones", {}).get("features", [])
    for i, feature in enumerate(features):
        zone_id = feature.get("zone_id", f"#{i}")
        try:
            geom = shape(feature["geometry"])
        except Exception as e:  # noqa: BLE001 - 壊れたジオメトリの内容をそのまま報告する
            errors.append(f"zone {zone_id}: ジオメトリを読めません: {e}")
            continue
        if geom.geom_type != "Polygon":
            errors.append(f"zone {zone_id}: 仕様は GeoJSON Polygon だが {geom.geom_type} になっている")
        if not geom.is_valid:
            from shapely.validation import explain_validity

            errors.append(f"zone {zone_id}: 無効なジオメトリ: {explain_validity(geom)}")
        if geom.geom_type == "Polygon":
            ring = "反時計回り" if geom.exterior.is_ccw else "時計回り"
            infos.append(f"zone {zone_id}: 外周は{ring}")
    return errors, infos


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    if not SCHEMA_DIR.is_dir():
        print(f"{SCHEMA_DIR} がありません。README.md の「翻訳元」の手順で原文を取得してください")
        return 2
    feed_dir = Path(sys.argv[1])
    files = sorted(feed_dir.glob("*.json"))
    if not files:
        print(f"{feed_dir} に JSON ファイルがありません")
        return 1

    failed = False
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"NG  {path.name}: JSON として読めません: {e}")
            failed = True
            continue

        errors = validate_schema(path, data)
        infos = []
        if path.name == "zones.json":
            zone_errors, infos = validate_zones(data)
            errors += zone_errors

        has_schema = (SCHEMA_DIR / path.name).exists()
        if errors:
            failed = True
            print(f"NG  {path.name}")
            for err in errors:
                print(f"      {err}")
        else:
            note = "" if has_schema else "（スキーマ無し: JSON 構文のみ確認）"
            print(f"OK  {path.name}{note}")
        for info in infos:
            print(f"    - {info}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

"""国土数値情報 行政区域データ（N03）から、北多摩交通圏サンプルの zones.json を作る。

使い方:
    .venv/bin/python tools/build_zones.py <N03 の GeoJSON> <出力する zones.json> [last_updated]

- kitatama: 北多摩交通圏の 15 市の和集合
- tokyo_mainland: 東京都のうち島しょ部（大島町〜小笠原村）を除いた区域（東京湾内の所属未定地を含む）の和集合
  東京湾の埋立地は運河で本土と分かれているが、GOFS の geometry は Polygon しか認めない。
  先行実装（ridefreebee）にならい、飛び地は本体から線をたどって飛び地を一周し、同じ線を戻る形で
  1 つの Polygon の外周に含める（自己接触する Polygon になる）。MIN_ISLAND_M2 未満の小さな飛び地は除く
- どちらも SIMPLIFY_M の許容誤差で簡略化し、外周リングを反時計回り（RFC 7946）、穴を時計回りにそろえる
加工方法の判断は notes/implementation-notes.md を参照。
"""

import json
import sys
import time
from math import cos, radians

import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon, shape
from shapely.geometry.polygon import orient
from shapely.ops import nearest_points, unary_union

KITATAMA = [
    "立川市", "府中市", "国立市", "調布市", "狛江市", "小金井市", "国分寺市", "小平市",
    "西東京市", "昭島市", "武蔵村山市", "東大和市", "東村山市", "清瀬市", "東久留米市",
]
ISLANDS = ["大島町", "利島村", "新島村", "神津島村", "三宅村", "御蔵島村", "八丈町", "青ヶ島村", "小笠原村"]

SIMPLIFY_M = 10  # 簡略化の許容誤差（m）
MIN_ISLAND_M2 = 10000  # これより小さい飛び地（岩礁・中州など）と穴（市区町村界のすき間など）は除く（m²）
MAINLAND_MIN_LAT = 35.4  # 所属未定地のうち、これより北（東京湾内）にあるものだけを本土側に含める
DIGITS = 6  # 座標の小数点以下の桁数（約 0.1m）

# 東京付近で度とメートルを近似的に換算する（簡略化・距離計算をメートル単位で行うため）
LAT0 = 35.7
KX = 111320 * cos(radians(LAT0))
KY = 110940


def to_m(g):
    return shapely.transform(g, lambda c: c * [KX, KY])


def to_deg(g):
    return shapely.transform(g, lambda c: np.round(c / [KX, KY], DIGITS))


def parts_of(g):
    parts = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
    return sorted(parts, key=lambda p: -p.area)


def ring_coords(ring):
    return [tuple(c) for c in ring.coords]


def insert_point(coords, pt):
    """閉じたリングの座標列に、リング上の点 pt を頂点として挿入し、その位置を返す。"""
    best = min(range(len(coords) - 1), key=lambda i: LineString(coords[i:i + 2]).distance(Point(pt)))
    coords.insert(best + 1, pt)
    return best + 1


def attach_islands(main, islands):
    """main の外周（または穴）から各飛び地へ往復線を引き、飛び地を 1 つのリングにつなぐ。

    往復線が他の飛び地を横切らないよう、つないだ部分に最も近い飛び地から順につなぐ。
    """
    main = orient(main, sign=1.0)
    rings = [ring_coords(main.exterior)] + [ring_coords(r) for r in main.interiors]
    holes_of_islands = []
    attached = [main]
    pending = [orient(p, sign=1.0) for p in islands]
    while pending:
        done = unary_union(attached)
        island = min(pending, key=lambda p: p.distance(done))
        pending.remove(island)
        a, b = nearest_points(done.boundary, island.exterior)
        a, b = a.coords[0], b.coords[0]
        # a が載っているリング（外周または穴）を探して挿入する
        target = min(range(len(rings)), key=lambda k: LineString(rings[k]).distance(Point(a)))
        ring = rings[target]
        i = insert_point(ring, a)
        isl = ring_coords(island.exterior)
        j = insert_point(isl, b)
        loop = isl[j:-1] + isl[:j] + [isl[j]]  # b から始まり b に戻る飛び地の外周（反時計回り）
        rings[target] = ring[:i + 1] + loop + ring[i:]
        holes_of_islands += [ring_coords(r) for r in island.interiors]
        attached.append(island)
    return Polygon(rings[0], rings[1:] + holes_of_islands)


def drop_small_holes(p):
    """市区町村界のすき間などでできた小さな穴を除く。"""
    return Polygon(p.exterior, [r for r in p.interiors if Polygon(r).area >= MIN_ISLAND_M2])


def build(geoms, label, allow_islands):
    union = unary_union(geoms).simplify(SIMPLIFY_M, preserve_topology=True)
    main, *rest = [drop_small_holes(p) for p in parts_of(union)]
    islands = [p for p in rest if p.area >= MIN_ISLAND_M2]
    dropped = [p for p in rest if p.area < MIN_ISLAND_M2]
    if rest and not allow_islands:
        sys.exit(f"{label}: 1 つの Polygon になりませんでした")
    poly_m = attach_islands(main, islands) if islands else orient(main, sign=1.0)
    poly = to_deg(poly_m)
    print(f"{label}: 飛び地 {len(islands)} 個を往復線でつないだ（除外 {len(dropped)} 個、計 約 "
          f"{sum(p.area for p in dropped):.0f} m2）。頂点数 {len(poly.exterior.coords)}、"
          f"穴 {len(poly.interiors)} 個、面積 約 {poly_m.area / 1e6:.1f} km2", file=sys.stderr)
    return poly


def main():
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    last_updated = int(sys.argv[3]) if len(sys.argv) == 4 else int(time.time())

    by_name = {}
    for f in json.load(open(src, encoding="utf-8"))["features"]:
        name, geom = f["properties"]["N03_004"], shape(f["geometry"])
        if name == "所属未定地" and geom.representative_point().y < MAINLAND_MIN_LAT:
            continue  # 伊豆・小笠原諸島の所属未定地
        by_name.setdefault(name, []).append(to_m(geom))

    missing = [c for c in KITATAMA if c not in by_name]
    if missing:
        sys.exit(f"N03 に見つからない市があります: {missing}")

    zones = [
        ("kitatama", "北多摩交通圏",
         build([g for c in KITATAMA for g in by_name[c]], "kitatama", allow_islands=False)),
        ("tokyo_mainland", "東京都（島しょ部を除く）",
         build([g for n, gs in by_name.items() if n not in ISLANDS for g in gs], "tokyo_mainland", allow_islands=True)),
    ]
    feed = {
        "last_updated": last_updated,
        "ttl": 86400,
        "version": "1.0",
        "data": {
            "zones": {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "zone_id": zid,
                        "properties": {"name": name},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[list(c) for c in poly.exterior.coords]]
                            + [[list(c) for c in r.coords] for r in poly.interiors],
                        },
                    }
                    for zid, name, poly in zones
                ],
            }
        },
    }
    with open(dst, "w", encoding="utf-8") as fp:
        json.dump(feed, fp, ensure_ascii=False, separators=(",", ":"))
        fp.write("\n")


if __name__ == "__main__":
    main()

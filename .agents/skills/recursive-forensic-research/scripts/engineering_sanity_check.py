"""Multi-Domain Engineering Sanity Check Tool (Research Harness² Scripts Component)

Provides rapid empirical and physical verification for:
1. Spatial Steel Structures (大跨度空间钢结构)
2. Supertall Towers & Wind/Seismic Mechanics (超高层建筑及抗风抗震力学)
3. Transit Hubs & Crowd Evacuation Dynamics (交通枢纽疏散与客流动力学)
"""

from __future__ import annotations

import argparse
import io
import json
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def check_spatial_structure(
    span_m: float,
    depth_m: float | None,
    area_m2: float,
    steel_tonnes: float,
    system_type: str = "truss",
) -> dict:
    """Checks basic aspect ratio and steel intensity for large-span spatial structures."""
    results = {
        "domain": "spatial_structures",
        "span_m": span_m,
        "area_m2": area_m2,
        "steel_tonnes": steel_tonnes,
        "steel_intensity_kg_per_m2": round((steel_tonnes * 1000) / area_m2, 2) if area_m2 > 0 else 0,
        "warnings": [],
        "verdict": "NORMAL",
    }

    # 1. Span-to-depth ratio checks
    if depth_m and depth_m > 0:
        ratio = round(span_m / depth_m, 2)
        results["span_to_depth_ratio"] = f"1/{ratio}"

        if system_type in ["truss", "space_frame"]:
            # Normal range for space truss: 1/12 to 1/20
            if ratio < 8:
                results["warnings"].append(
                    f"截面高厚比异常粗壮 (1/{ratio} > 1/8)，可能存在过量用钢或承受极端局部重荷载。"
                )
            elif ratio > 25:
                results["warnings"].append(
                    f"截面高厚比偏轻薄 (1/{ratio} < 1/25)，需重点核查竖向刚度、活荷载挠度及风致颤振安全裕度。"
                )
        elif system_type in ["cable_net", "spoke_wheel"]:
            # Spoke wheel sag/depth to span ratio: 1/10 to 1/25
            if ratio > 30:
                results["warnings"].append(
                    f"索网矢跨比/索桁高跨比过小 (1/{ratio})，索端锚固预拉力将极其巨大，对环梁抗压能力要求极高。"
                )

    # 2. Steel intensity checks
    intensity = results["steel_intensity_kg_per_m2"]
    if system_type in ["cable_net", "tensile_membrane"]:
        # Lightweight tensile systems normally 25 - 80 kg/m2 (excluding concrete ring)
        if intensity > 120:
            results["warnings"].append(
                f"轻量索网/膜结构用钢指标偏高 ({intensity} kg/m²)，可能计入了外周重型悬挑钢桅杆或压环梁重量。"
            )
    elif system_type in ["retractable_roof", "heavy_truss"]:
        # Heavy movable / retractable roofs normally 120 - 280+ kg/m2
        if intensity < 60:
            results["warnings"].append(
                f"可开合/重型空间桁架用钢指标偏低 ({intensity} kg/m²)，疑似仅统计了移动扇叶部分，漏计固定支承主桁架。"
            )
        elif intensity > 350:
            results["warnings"].append(
                f"单位用钢量超高 ({intensity} kg/m²)，可能包含巨型设备悬吊、特重防爆或深覆土/草坪地宫钢托盘自重。"
            )

    if results["warnings"]:
        results["verdict"] = "CAUTION: NEED_CROSS_EXAMINATION"

    return results


def check_supertall_mechanics(
    height_m: float,
    base_width_m: float,
    gross_area_m2: float,
    floors: int,
    steel_tonnes: float | None = None,
) -> dict:
    """Checks slenderness ratio, approximate fundamental period, and gravity load indices for supertall buildings."""
    aspect_ratio = round(height_m / base_width_m, 2)
    # Fundamental natural period empirical estimate T1 ≈ 0.1 * N (floors) or 0.02 ~ 0.03 * H(m)
    approx_t1_sec = round(height_m * 0.025, 2)

    results = {
        "domain": "supertall_mechanics",
        "height_m": height_m,
        "base_width_m": base_width_m,
        "aspect_ratio": f"{aspect_ratio}:1",
        "estimated_period_t1_sec": approx_t1_sec,
        "warnings": [],
        "verdict": "NORMAL",
    }

    # 1. Aspect ratio (高宽比) verification
    if aspect_ratio > 9.0:
        results["warnings"].append(
            f"极端细长比 ({aspect_ratio}:1 > 9:1)，必须配置外伸伸臂桁架（Outriggers）、巨柱体系（Mega-columns）及顶置TMD调谐质量阻尼器。"
        )
    elif aspect_ratio > 7.0:
        results["warnings"].append(
            f"高细长比 ({aspect_ratio}:1 > 7:1)，受风荷载涡激共振控制显著，需重点核查侧移角（1/500限值）及顶部风振舒适度加速度。"
        )

    # 2. Structural steel index if provided
    if steel_tonnes and gross_area_m2 > 0:
        steel_intensity = round((steel_tonnes * 1000) / gross_area_m2, 2)
        results["steel_intensity_kg_per_m2"] = steel_intensity
        # Supertall steel-concrete composite towers typically 70 - 180 kg/m2 of structural steel
        if steel_intensity < 50:
            results["warnings"].append(
                f"超高层单位用钢量偏低 ({steel_intensity} kg/m²)，疑似仅统计了内筒钢构，未计外框巨型钢管混凝土柱（CFT）用钢。"
            )
        elif steel_intensity > 250:
            results["warnings"].append(
                f"超高层单位用钢量超高 ({steel_intensity} kg/m²)，应为全纯钢框架或位于超强抗震烈度区。"
            )

    if results["warnings"]:
        results["verdict"] = "CAUTION: ADVANCED_AERODYNAMICS_REQUIRED"

    return results


def check_transit_evacuation(
    capacity_persons: int,
    total_exit_width_m: float,
    max_evac_distance_m: float,
    design_time_limit_min: float = 8.0,
) -> dict:
    """Checks rapid crowd evacuation capacity according to international codes (NFPA 130 / GB 50016 / Green Guide)."""
    # Unit flow rate: typically 75 - 90 persons / minute / meter of clear door width
    unit_flow_rate = 80.0  # persons/min/meter
    max_throughput_per_min = round(total_exit_width_m * unit_flow_rate, 1)
    required_time_min = round(capacity_persons / max_throughput_per_min, 2) if max_throughput_per_min > 0 else 999.0

    # Evacuation walking time: average crowd walking speed under density ≈ 0.8 m/s (48 m/min)
    walk_speed_m_per_min = 48.0
    walk_travel_time_min = round(max_evac_distance_m / walk_speed_m_per_min, 2)
    total_estimated_evac_time_min = round(required_time_min + (walk_travel_time_min * 0.5), 2)

    results = {
        "domain": "transit_and_evacuation",
        "capacity_persons": capacity_persons,
        "total_exit_width_m": total_exit_width_m,
        "design_time_limit_min": design_time_limit_min,
        "calculated_bottleneck_time_min": required_time_min,
        "total_estimated_evac_time_min": total_estimated_evac_time_min,
        "warnings": [],
        "verdict": "NORMAL",
    }

    if total_estimated_evac_time_min > design_time_limit_min:
        results["warnings"].append(
            f"疏散预计耗时 ({total_estimated_evac_time_min} 分钟) 超出设计安全时限 ({design_time_limit_min} 分钟)。出口宽度或通道存在严重瓶颈！"
        )
        results["verdict"] = "DEFICIENT: CAPACITY_BOTTLENECK"
    elif total_estimated_evac_time_min > design_time_limit_min * 0.85:
        results["warnings"].append(
            f"疏散裕度偏低（达设计时限的 {round(total_estimated_evac_time_min/design_time_limit_min*100, 1)}%），遇拥挤推挤恐有安全隐患。"
        )

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Domain Engineering Sanity Check CLI")
    subparsers = parser.add_subparsers(dest="domain", required=True)

    # Spatial parser
    p_spatial = subparsers.add_parser("spatial", help="Spatial steel & roof structures")
    p_spatial.add_argument("--span", type=float, required=True, help="Span in meters")
    p_spatial.add_argument("--depth", type=float, default=None, help="Structural depth in meters")
    p_spatial.add_argument("--area", type=float, required=True, help="Covered area in m2")
    p_spatial.add_argument("--steel", type=float, required=True, help="Steel weight in metric tonnes")
    p_spatial.add_argument(
        "--type",
        choices=["truss", "space_frame", "cable_net", "spoke_wheel", "retractable_roof", "tensile_membrane"],
        default="truss",
        help="System type",
    )

    # Supertall parser
    p_supertall = subparsers.add_parser("supertall", help="Supertall tower mechanics")
    p_supertall.add_argument("--height", type=float, required=True, help="Total height in meters")
    p_supertall.add_argument("--width", type=float, required=True, help="Base width in meters")
    p_supertall.add_argument("--area", type=float, required=True, help="Gross floor area in m2")
    p_supertall.add_argument("--floors", type=int, required=True, help="Number of above-ground floors")
    p_supertall.add_argument("--steel", type=float, default=None, help="Structural steel weight in tonnes")

    # Transit parser
    p_transit = subparsers.add_parser("transit", help="Transit hub and arena crowd evacuation")
    p_transit.add_argument("--capacity", type=int, required=True, help="Max design capacity (persons)")
    p_transit.add_argument("--width", type=float, required=True, help="Sum of clear exit doors width in meters")
    p_transit.add_argument("--distance", type=float, required=True, help="Max egress travel distance in meters")
    p_transit.add_argument("--limit", type=float, default=8.0, help="Egress time limit in minutes")

    args = parser.parse_args()

    if args.domain == "spatial":
        res = check_spatial_structure(
            span_m=args.span,
            depth_m=args.depth,
            area_m2=args.area,
            steel_tonnes=args.steel,
            system_type=args.type,
        )
    elif args.domain == "supertall":
        res = check_supertall_mechanics(
            height_m=args.height,
            base_width_m=args.width,
            gross_area_m2=args.area,
            floors=args.floors,
            steel_tonnes=args.steel,
        )
    elif args.domain == "transit":
        res = check_transit_evacuation(
            capacity_persons=args.capacity,
            total_exit_width_m=args.width,
            max_evac_distance_m=args.distance,
            design_time_limit_min=args.limit,
        )
    else:
        print(f"Unknown domain: {args.domain}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

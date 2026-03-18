#!/usr/bin/env python3
"""Export ESCAPE 36 baseline to CSV and metadata.

Generates: lcoga_vs_q.csv, annual_production.csv, cost_breakdown_by_block.csv,
cost_breakdown_by_step.csv, q_star.csv, metadata.json.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tea_model_ga_escape36 as tea
from config.escape36_config import ESCAPE_BASELINE

OUT_DIR = REPO_ROOT / "outputs" / "csv"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ROUTES = ("IX", "SX")
EXPORT_Q_VALUES = (10, 20, 50, 100)


def _q_star(Q_grid, lco_arr, price):
    """Return Q* where LCOGa <= price (linear interpolation)."""
    if float(lco_arr[0]) <= float(price):
        return float(Q_grid[0])
    if float(lco_arr[-1]) > float(price):
        return None
    for i in range(len(Q_grid) - 1):
        y0, y1 = float(lco_arr[i]), float(lco_arr[i + 1])
        if (y0 - price) * (y1 - price) <= 0:
            q0, q1 = float(Q_grid[i]), float(Q_grid[i + 1])
            if y1 == y0:
                return q0
            return q0 + (price - y0) * (q1 - q0) / (y1 - y0)
    return None


def main():
    config = ESCAPE_BASELINE
    market_price = config.ga_market_price_base
    q_grid = list(range(1, 101))

    # lcoga_vs_q.csv
    rows = []
    for q in EXPORT_Q_VALUES:
        lco_ix = tea.calc_lco_ga(float(q), route="IX", config=config)
        lco_sx = tea.calc_lco_ga(float(q), route="SX", config=config)
        rows.append({
            "Q_m3_per_d": q,
            "LCOGa_IX_EUR_per_kg": round(lco_ix, 6),
            "LCOGa_SX_EUR_per_kg": round(lco_sx, 6),
            "market_price_EUR_per_kg": market_price,
        })
    _write_csv(
        OUT_DIR / "lcoga_vs_q.csv",
        ["Q_m3_per_d", "LCOGa_IX_EUR_per_kg", "LCOGa_SX_EUR_per_kg", "market_price_EUR_per_kg"],
        rows,
    )

    # annual_production.csv
    rows = []
    for q in EXPORT_Q_VALUES:
        prod_ix = tea.calc_annual_production(float(q), route="IX", config=config)
        prod_sx = tea.calc_annual_production(float(q), route="SX", config=config)
        rows.append({
            "Q_m3_per_d": q,
            "annual_prod_IX_kg_per_yr": round(prod_ix, 6),
            "annual_prod_SX_kg_per_yr": round(prod_sx, 6),
        })
    _write_csv(
        OUT_DIR / "annual_production.csv",
        ["Q_m3_per_d", "annual_prod_IX_kg_per_yr", "annual_prod_SX_kg_per_yr"],
        rows,
    )

    # cost_breakdown_by_block.csv
    block_keys = ["CapEx-Sep", "CapEx-Other", "OpEx", "Repl-Sep", "Repl-Other", "Labour", "CO2_Tax"]
    rows = []
    for q in EXPORT_Q_VALUES:
        for route in ROUTES:
            cb = tea.calc_cost_breakdown(float(q), route=route, config=config)
            rows.append({
                "Q_m3_per_d": q,
                "route": route,
                **{k: round(cb[k], 6) for k in block_keys},
            })
    _write_csv(OUT_DIR / "cost_breakdown_by_block.csv", ["Q_m3_per_d", "route"] + block_keys, rows)

    # cost_breakdown_by_step.csv
    rows = []
    for q in EXPORT_Q_VALUES:
        for route in ROUTES:
            costs = tea.calc_total_costs(float(q), route=route, config=config)
            for step, values in costs.items():
                if step == "Total":
                    continue
                rows.append({
                    "Q_m3_per_d": q,
                    "route": route,
                    "step": step,
                    "CapEx": round(values["CapEx"], 6),
                    "REP": round(values["REP"], 6),
                    "OpEx": round(values["OpEx"], 6),
                })
    _write_csv(
        OUT_DIR / "cost_breakdown_by_step.csv",
        ["Q_m3_per_d", "route", "step", "CapEx", "REP", "OpEx"],
        rows,
    )

    # q_star.csv
    lco_ix_arr = [tea.calc_lco_ga(float(q), route="IX", config=config) for q in q_grid]
    lco_sx_arr = [tea.calc_lco_ga(float(q), route="SX", config=config) for q in q_grid]
    q_star_ix = _q_star(q_grid, lco_ix_arr, market_price)
    q_star_sx = _q_star(q_grid, lco_sx_arr, market_price)
    rows = [
        {"route": "IX", "q_break_even_m3_per_d": q_star_ix if q_star_ix is not None else ""},
        {"route": "SX", "q_break_even_m3_per_d": q_star_sx if q_star_sx is not None else ""},
    ]
    _write_csv(OUT_DIR / "q_star.csv", ["route", "q_break_even_m3_per_d"], rows)

    # metadata.json
    metadata = {
        "baseline_id": "escape36_final",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "co2_tax_mode": config.co2_tax_mode,
        "co2_tax_per_ton": config.co2_tax_per_ton,
        "sx_makeup_rate_annual": config.sx_makeup_rate_annual,
        "c_ga_feed_mg_L": tea.FEED_BASELINE_TEMPLATE["species_mg_L"]["Ga"],
        "ga_market_price_base": config.ga_market_price_base,
        "model_file": "tea_model_ga_escape36.py",
    }
    with (REPO_ROOT / "outputs" / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Exports written to outputs/csv/")
    print(f"  lcoga_vs_q.csv, annual_production.csv, cost_breakdown_by_block.csv,")
    print(f"  cost_breakdown_by_step.csv, q_star.csv")
    print(f"  metadata.json -> outputs/")


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""ESCAPE 36: LCOGa vs throughput Q for IX and SX routes.

Single panel with market price line at 423 €/kg.
Uses ESCAPE baseline (no CO₂ tax).
"""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import tea_model_ga_escape36 as tea
from config.escape36_config import ESCAPE_BASELINE

OUT_FIGURES = REPO_ROOT / "outputs" / "figures"
OUT_FIGURES.mkdir(parents=True, exist_ok=True)

COLOR_IX = "#00549F"
COLOR_SX = "#8EBAE5"
COLOR_MARKET = "#64748b"

CM_TO_IN = 1 / 2.54
FIG_W = 12 * CM_TO_IN
FIG_H = FIG_W * 0.78


def _set_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "svg.fonttype": "none",
        "axes.grid": True,
        "grid.alpha": 0.30,
        "grid.linestyle": "--",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })


def main():
    config = ESCAPE_BASELINE
    market_price = config.ga_market_price_base
    q_grid = np.linspace(10, 100, 91)

    lco_ix = np.array([tea.calc_lco_ga(float(q), route="IX", config=config) for q in q_grid])
    lco_sx = np.array([tea.calc_lco_ga(float(q), route="SX", config=config) for q in q_grid])

    _set_style()
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))

    ax.plot(q_grid, lco_ix, color=COLOR_IX, linewidth=2, label="IX")
    ax.plot(q_grid, lco_sx, color=COLOR_SX, linewidth=2, label="SX")
    ax.axhline(market_price, color=COLOR_MARKET, linestyle="--", linewidth=1, alpha=0.8, label=f"{market_price:.0f} €/kg")

    ax.set_xlabel(r"Throughput Q [m$^3$ d$^{-1}$]")
    ax.set_ylabel(r"LCOGa [€ kg$^{-1}$]")
    ax.set_title("Levelised cost of gallium vs throughput (ESCAPE 36 baseline)")
    ax.set_xlim(10, 100)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    out_path = OUT_FIGURES / "lcoga_vs_q.svg"
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)

    print(f"  -> {out_path.name}")


if __name__ == "__main__":
    main()

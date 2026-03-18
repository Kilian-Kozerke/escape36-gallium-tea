#!/usr/bin/env python3
"""ESCAPE 36 Figure 2A: Annual production vs throughput Q (log-log).

IX and SX routes. Uses ESCAPE baseline (no CO₂ tax).
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

OUT_FIGURES = REPO_ROOT / "outputs" / "figures"
OUT_FIGURES.mkdir(parents=True, exist_ok=True)

COLOR_IX = "#00549F"
COLOR_SX = "#8EBAE5"

CM_TO_IN = 1 / 2.54
FIG_W = 12 * CM_TO_IN
FIG_H = FIG_W * 0.78

ROUTE_STYLE = {
    "IX": {"color": COLOR_IX, "linestyle": "-", "marker": "o"},
    "SX": {"color": COLOR_SX, "linestyle": "--", "marker": "s"},
}


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
    config = tea.DEFAULT_CONFIG
    Q = tea.Q_FEED_RANGE.astype(float)

    prod_ix = np.array([tea.calc_annual_production(float(q), route="IX", config=config) for q in Q])
    prod_sx = np.array([tea.calc_annual_production(float(q), route="SX", config=config) for q in Q])

    _set_style()
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))

    for route, prod in [("IX", prod_ix), ("SX", prod_sx)]:
        st = ROUTE_STYLE[route]
        ax.loglog(
            Q,
            prod,
            label=f"{route} Route",
            color=st["color"],
            linestyle=st["linestyle"],
            marker=st["marker"],
            linewidth=2.4,
            markersize=4.8,
        )

    ax.set_xlabel(r"Feed flow rate [m$^3$ day$^{-1}$]")
    ax.set_ylabel(r"Annual production rate [kg yr$^{-1}$]")
    ax.set_title("Annual production rate vs. feed flow rate", pad=4)
    ax.legend(loc="upper left", frameon=False)
    fig.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.18)

    out_path = OUT_FIGURES / "figure2a_production.svg"
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)

    print(f"  -> {out_path.name}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""ESCAPE 36 Figure 2B: LCOGa vs throughput Q (log-x).

1:1 clone of export_fig2_panels.export_panel_b (TEA/figures/paper_support/).
Data: tea_model_ga_escape36.calc_lco_ga() at Q_FEED_RANGE points.
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

OUT_FIGURES = REPO_ROOT / "outputs" / "figures"
OUT_FIGURES.mkdir(parents=True, exist_ok=True)

# Exact match: export_fig2_panels.py PALETTE, ROUTE_STYLE, dimensions
PALETTE = {
    "blue_dark": "#00549F",
    "blue_light": "#8EBAE5",
    "black": "#000000",
}
ROUTE_STYLE = {
    "IX": {"color": PALETTE["blue_dark"], "linestyle": "-", "marker": "o"},
    "SX": {"color": PALETTE["blue_light"], "linestyle": "--", "marker": "s"},
}

CM_TO_IN = 1.0 / 2.54
FIG_W_CM = 7.5  # same as export_fig2_panels (screenshot source)
FIG_W_IN = FIG_W_CM * CM_TO_IN
FIG_H_IN = FIG_W_IN * 0.78


def _set_style():
    """Unified style: Arial 8pt, identical to export_fig2_panels._set_style()."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "mathtext.fontset": "dejavusans",
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
    market_price = config.ga_market_price_base
    Q = tea.Q_FEED_RANGE.astype(float)

    lco_ix = np.array([tea.calc_lco_ga(float(q), route="IX", config=config) for q in Q])
    lco_sx = np.array([tea.calc_lco_ga(float(q), route="SX", config=config) for q in Q])

    _set_style()
    fig, ax = plt.subplots(figsize=(FIG_W_IN, FIG_H_IN))

    for route, lco in [("IX", lco_ix), ("SX", lco_sx)]:
        st = ROUTE_STYLE[route]
        ax.semilogx(
            Q,
            lco,
            label=f"{route} Route",
            color=st["color"],
            linestyle=st["linestyle"],
            marker=st["marker"],
            linewidth=2.4,
            markersize=4.8,
        )

    ax.axhline(y=market_price, color=PALETTE["black"], linestyle=":", linewidth=1.8)
    ax.text(
        0.98,
        0.70,
        f"Market price: {market_price:.0f} €/kg Ga 4N",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        color=PALETTE["black"],
    )

    ax.set_xlabel(r"Feed flow rate [m$^3$ day$^{-1}$]")
    ax.set_ylabel(r"LCOGa [€ kg$^{-1}$]")
    ax.set_title("B) Levelized cost of Ga\nvs. feed flow rate", pad=4)
    ax.legend(loc="upper right", frameon=False)
    fig.subplots_adjust(left=0.18, right=0.98, top=0.84, bottom=0.22)

    out_path = OUT_FIGURES / "figure2b_lcoga.svg"
    fig.savefig(out_path, format="svg", facecolor="white", bbox_inches=None, pad_inches=0)
    plt.close(fig)

    print(f"  -> {out_path.name}")


if __name__ == "__main__":
    main()

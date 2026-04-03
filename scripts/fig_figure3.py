#!/usr/bin/env python3
"""ESCAPE 36 Figure 3: Cost breakdown (stacked bar) at Q=10 and Q=100.

Relative contribution to LCOGa: CapEx, OpEx, Replacement, Labour.
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
from matplotlib.patches import Patch

import tea_model_ga_escape36 as tea

OUT_FIGURES = REPO_ROOT / "outputs" / "figures"
OUT_FIGURES.mkdir(parents=True, exist_ok=True)

BLOCK_ORDER = ["CapEx", "OpEx", "Replacement", "Labour"]
BLOCK_COLORS = {
    "CapEx": "#00549F",
    "OpEx": "#57AB27",
    "Replacement": "#F6A800",
    "Labour": "#808080",
}

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
    config = tea.DEFAULT_CONFIG
    bars = [("IX", 10.0), ("SX", 10.0), ("IX", 100.0), ("SX", 100.0)]
    x_labels = [f"{r}@{int(q)}" for r, q in bars]

    pct_by_bar = []
    for route, q in bars:
        cb = tea.calc_cost_breakdown(q, route=route, config=config)
        capex = cb["CapEx-Sep"] + cb["CapEx-Other"]
        repl = cb["Repl-Sep"] + cb["Repl-Other"]
        total = capex + cb["OpEx"] + repl + cb["Labour"]
        pct_by_bar.append({
            "CapEx": capex / total * 100,
            "OpEx": cb["OpEx"] / total * 100,
            "Replacement": repl / total * 100,
            "Labour": cb["Labour"] / total * 100,
        })

    _set_style()
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    x = np.arange(len(bars))
    bottoms = np.zeros(len(bars))

    for block in BLOCK_ORDER:
        vals = np.array([p[block] for p in pct_by_bar])
        ax.bar(x, vals, bottom=bottoms, color=BLOCK_COLORS[block],
               width=0.72, edgecolor="white", linewidth=0.6, label=block)
        for xi, btm, v in zip(x, bottoms, vals):
            if v >= 5.0:
                ax.text(xi, btm + v / 2, f"{v:.0f}%",
                        ha="center", va="center", fontsize=8, fontweight="bold",
                        color="white" if block in ["CapEx", "Labour", "OpEx"] else "black")
        bottoms += vals

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Relative contribution\nto LCOGa [%]", labelpad=2)
    ax.set_title("Cost contribution (Q=10 vs 100)", pad=4)
    handles = [Patch(facecolor=BLOCK_COLORS[b], label=b) for b in BLOCK_ORDER]
    ax.legend(handles=handles, loc="upper center", ncol=4, frameon=False,
              bbox_to_anchor=(0.5, -0.12), borderaxespad=0.0)
    fig.subplots_adjust(left=0.26, right=0.98, top=0.88, bottom=0.28)

    out_path = OUT_FIGURES / "figure3_cost_breakdown.svg"
    fig.savefig(out_path, format="svg", bbox_inches="tight")
    plt.close(fig)

    print(f"  -> {out_path.name}")


if __name__ == "__main__":
    main()

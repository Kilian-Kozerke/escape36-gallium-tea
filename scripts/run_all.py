#!/usr/bin/env python3
"""Master runner for ESCAPE 36 baseline exports and figures.

Run from repo root: python scripts/run_all.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
for p in (str(REPO_ROOT), str(SCRIPTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import export_baseline
import fig_figure2a
import fig_figure2b
import fig_figure3


def main():
    print("=" * 60)
    print("ESCAPE 36 Gallium TEA – Baseline export and figures")
    print("=" * 60)
    print()

    print("Exporting CSVs and metadata...")
    export_baseline.main()
    print()

    print("Generating Figure 2A (production, log-log)...")
    fig_figure2a.main()
    print()

    print("Generating Figure 2B (LCOGa, log-x)...")
    fig_figure2b.main()
    print()

    print("Generating Figure 3 (cost breakdown)...")
    fig_figure3.main()
    print()

    print("=" * 60)
    print("Done. Outputs: outputs/csv/, outputs/figures/, outputs/metadata.json")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

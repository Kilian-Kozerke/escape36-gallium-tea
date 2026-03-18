"""ESCAPE 36 paper baseline configuration.

Carbon costs (CO₂ tax, LCA) are out of scope for the conference paper.
DEFAULT_CONFIG in tea_model_ga_escape36 already has co2_tax_mode='none'.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tea_model_ga_escape36 as tea

ESCAPE_BASELINE = tea.DEFAULT_CONFIG

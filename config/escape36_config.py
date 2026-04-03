"""ESCAPE 36 paper baseline configuration."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tea_model_ga_escape36 as tea

ESCAPE_BASELINE = tea.DEFAULT_CONFIG

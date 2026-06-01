"""
run_sample.py
─────────────
One-shot helper that runs the recommendation engine with the
sample query "python ai machine learning automation" and saves
the result to outputs/sample_output.txt.

Run with:
    python run_sample.py
"""

import os, sys

# ── patch stdin so main() receives our preset input ───────────────
import io
SAMPLE_INPUT = "python ai machine learning automation\nno\n"
sys.stdin = io.StringIO(SAMPLE_INPUT)

# ── run main ──────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from main import main
main()

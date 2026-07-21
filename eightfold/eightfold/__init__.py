"""Eightfold v1 — the charge atlas of computational problems.

Rows are natural computational problems under fixed encodings; columns are eight literature-sourced hardness
"charges" (decision, counting, approximation, parameterized, parallelization, proof-size, average-case,
landscape/freezing). Every cell carries a value + a citation, or an explicit open/unmeasured/n.a. flag.
Structure detection looks for multiplets, forbidden regions, and gaps. See AGENTS.md.

Third project in the proof-space line (Desert Map → Proof Census → Eightfold). Core (atlas.py) is
stdlib-only; the categorical-statistics harness (structure.py) lives behind the [analysis] extra.
"""

__version__ = "0.1.0"

"""Desert Map — Proof-Space Cartography v1.

Package import stays torch-free: the oracle path (instance / verify / fixtures) must import with no ML
stack. The relaxation engine (relax / losses / run / hessian) lazy-imports torch only when used.
See AGENTS.md invariant 1.
"""

__version__ = "0.1.0"

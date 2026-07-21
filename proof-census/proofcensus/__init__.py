"""Proof Census v1 — population map of the refutation set of unsat random 3-SAT.

Samples many valid Resolution refutations per instance with two structurally-different randomized samplers
(S1 constructive-saturation DAG, S2 DPLL tree-resolution), gates every proof through the frozen desert-map
M1 verifier, and computes population statistics. All claims are sampler-relative. See AGENTS.md.
"""

__version__ = "0.1.0"

"""Thin per-claim adapters: the only glue between the manifest and the research
packages. Each adapter returns a flat ``dict[str, value]`` of the numbers a claim
asserts. Fast adapters recompute from the frozen committed artifacts (atlas,
checkpoint, matrices) via the real helpers where cheap, or read the committed
result where recomputation is expensive; ``full`` adapters regenerate.
"""

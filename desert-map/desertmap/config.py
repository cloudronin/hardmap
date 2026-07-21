"""HF execution config for desert-map — repo ids, GPU flavors, base image (env-overridable).

Everything here is `os.environ.get(..., default)` so nothing is hardcoded. The default repo ids are
PLACEHOLDERS ("<hf-user>/..."); set the real ids via env when the HF key is dropped, e.g.:

    export DESERTMAP_HF_RESULTS="myuser/desert-map-results"
    export DESERTMAP_HF_HARNESS="myuser/desert-map-harness"

Confirm exact GPU flavor strings at build time with `hf jobs hardware` (spec I5).
"""
from __future__ import annotations

import os

# Private HF dataset repos the run reads/writes.
# HARNESS_REPO: the code mirror the container fetches (so a job runs the pinned harness).
# RESULTS_REPO: per-cell metrics (parquet) + converged proof tensors + decoded proofs + manifest.
HARNESS_REPO = os.environ.get("DESERTMAP_HF_HARNESS", "<hf-user>/desert-map-harness")
RESULTS_REPO = os.environ.get("DESERTMAP_HF_RESULTS", "<hf-user>/desert-map-results")

# GPU flavors (confirm exact strings via `hf jobs hardware`). Per spec I5:
#   T4-small for E0/smoke, 1x L4 for E1/E2/E4, L40S only if E4 L=8n OOMs, CPU-upgrade for M1 fixtures.
FLAVOR_SMOKE = os.environ.get("DESERTMAP_FLAVOR_SMOKE", "t4-small")     # E0 / smoke round-trip
FLAVOR_SWEEP = os.environ.get("DESERTMAP_FLAVOR_SWEEP", "l4x1")         # E1 / E2 / E4 default
FLAVOR_BIG = os.environ.get("DESERTMAP_FLAVOR_BIG", "l40sx1")           # E4 L=8n fallback (OOM)
FLAVOR_CPU = os.environ.get("DESERTMAP_FLAVOR_CPU", "cpu-upgrade")      # M1 fixtures / E5 analysis

# Base image. Desert Map has NO vLLM — a plain pytorch runtime image ships torch preinstalled, so the
# container bootstrap only pip-installs the light extras (numpy, python-sat, scipy, huggingface_hub,
# pyarrow). Confirm the tag pulls reliably on HF runners at build time; the raitune note (pytorch
# *-devel ~7GB flaked with ErrImagePull) is why we pick the smaller -runtime image, not -devel.
IMAGE = os.environ.get("DESERTMAP_IMAGE", "pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime")

# HARD job timeout (seconds) = the cost cap. HF default is 30 min; always pass an explicit value.
DEFAULT_TIMEOUT = int(os.environ.get("DESERTMAP_TIMEOUT", str(2 * 60 * 60)))

# HF token location for a FUTURE launcher (v1 is killed at M2 — nothing here submits jobs yet). The token is
# read from $HF_TOKEN or this file at submit time and never placed on the command line (raitune pattern); the
# file lives outside the repo and its contents are never read into logs or committed. Default points at the
# path the key was dropped at; override with DESERTMAP_HF_KEY_FILE.
KEY_PATH = os.environ.get("DESERTMAP_HF_KEY_FILE", "/tmp/HUGGING_FACE_KEY.txt")


def read_token() -> str | None:
    """Return the HF token from $HF_TOKEN or KEY_PATH, or None. For a future launcher; unused in v1."""
    import pathlib
    tok = os.environ.get("HF_TOKEN")
    if tok:
        return tok.strip()
    p = pathlib.Path(KEY_PATH)
    return p.read_text().strip() if p.is_file() else None

"""HF Jobs launch + in-container entrypoint for desert-map sweeps.

Mirrors raitune/raitune/hf/ — pure (unit-tested) argv + bootstrap builders in launcher.py, a stable
narrow-permission CLI in launch.py, and the in-container program in entrypoint.py. Simplified: no
vLLM/serving/judge — Desert Map is pure numerical PyTorch.
"""

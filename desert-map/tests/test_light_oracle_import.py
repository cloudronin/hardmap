"""AGENTS.md invariant 1: the oracle path (instance / verify / fixtures) must import with NO ML stack.

Enforced in a subprocess that installs a meta-path hook raising ImportError on any attempt to import
torch; importing the oracle modules there must still succeed. (Mirrors raitune's
test_no_heavy_core_import.)"""
from __future__ import annotations

import subprocess
import sys

_CODE = r"""
import sys
class _BlockTorch:
    def find_spec(self, name, path=None, target=None):
        if name == "torch" or name.startswith("torch."):
            raise ImportError("torch import is forbidden in the oracle path")
        return None
sys.meta_path.insert(0, _BlockTorch())
import desertmap.verify        # noqa: F401
import desertmap.instance      # noqa: F401
import desertmap.fixtures      # noqa: F401
assert "torch" not in sys.modules, "torch was imported by the oracle path"
print("OK")
"""


def test_oracle_imports_without_torch():
    r = subprocess.run([sys.executable, "-c", _CODE], capture_output=True, text=True)
    assert r.returncode == 0, f"oracle import pulled torch or failed:\nSTDOUT:{r.stdout}\nSTDERR:{r.stderr}"
    assert r.stdout.strip().endswith("OK")

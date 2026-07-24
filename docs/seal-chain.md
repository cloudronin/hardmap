# Seal chain -- uofa-lab -> hardmap

The program's epistemic argument rests on *sealed-before-measured*: each preregistration was sealed by the act of committing it (`committed_before_analysis: true`), so the seal **is** the commit SHA that introduced the prereg. Consolidation extracted the four in-scope folders with `git filter-repo`, which rewrites commit hashes. This table resolves every sealed prereg end to end -- *sealed at X (public: Y)* -- via `docs/hash-map.txt`.

Source: private predecessor monorepo `uofa-lab`. Commits: 130 rewritten, 329 pruned (out-of-scope only).

## Atlas provenance

The frozen `atlas.jsonl` carries `code_commit: uofa-lab@55c7df5` (preserved byte-identically). It resolves to:

- `uofa-lab@55c7df5` -> `hardmap@3581db3`  (full: `3581db30a6880d7f15cc09184456ac2de7d1d3a7`)

## Sealed preregistrations

| folder | prereg | sealed (uofa-lab) | public (hardmap) | date | status |
|---|---|---|---|---|---|
| eightfold | prereg_v1.json | `d40bde0b0` | `6909e9192` | 2026-07-21 | ok |
| eightfold | prereg_v2.json | `d40bde0b0` | `6909e9192` | 2026-07-21 | ok |
| eightfold | prereg_v3.json | `d40bde0b0` | `6909e9192` | 2026-07-21 | ok |
| eightfold | prereg_v4.json | `3b30b9a11` | `9f8e0ecc9` | 2026-07-21 | ok |
| eightfold | prereg_v5.json | `040d91cf7` | `e31264ffc` | 2026-07-21 | ok |
| eightfold | prereg_v6.json | `759784702` | `baf2c761b` | 2026-07-21 | ok |
| eightfold | prereg_v7.json | `fff8a3294` | `e06ccad30` | 2026-07-21 | ok |
| eightfold | prereg_v8.json | `3922d0e47` | `bb79134ba` | 2026-07-21 | ok |
| foundry | prereg_v1.json | `694e463ee` | `8b060949c` | 2026-07-21 | ok |
| foundry | prereg_v2.json | `9a3bc8297` | `a1c5544d1` | 2026-07-21 | ok |
| foundry | prereg_v3.json | `e61665cdb` | `058ffa1fa` | 2026-07-22 | ok |
| foundry | prereg_v4.json | `aed3c6297` | `21d888ae3` | 2026-07-22 | ok |
| foundry | prereg_v5.json | `1fbdab7d6` | `494186b9f` | 2026-07-22 | ok |
| foundry | prereg_v6.json | `46b331f00` | `4b0f2f163` | 2026-07-22 | ok |
| foundry | prereg_v7.json | `e0113b3ec` | `2af33085e` | 2026-07-22 | ok |
| foundry | prereg_v8.json | `5eecc7ca7` | `62367358c` | 2026-07-22 | ok |
| foundry | prereg_v9.json | `e86eb0a49` | `07a3a26d7` | 2026-07-22 | ok |
| foundry | prereg_v10.json | `cef650f43` | `3769bf2b9` | 2026-07-22 | ok |
| foundry | prereg_v11.json | `d4deacdd3` | `0e299c185` | 2026-07-22 | ok |
| foundry | prereg_v12.json | `f8c8cf7c4` | `dffe05fa8` | 2026-07-22 | ok |
| foundry | prereg_v13.json | `3ec361715` | `12adc88df` | 2026-07-22 | ok |
| foundry | prereg_v14.json | `12746e872` | `56f7a8d75` | 2026-07-22 | ok |
| foundry | prereg_v15.json | `16c4c2f94` | `5e35ebe25` | 2026-07-22 | ok |
| foundry | prereg_v16.json | `f0c97e726` | `35a684e27` | 2026-07-22 | ok |
| foundry | prereg_v17.json | `5bab4a536` | `4ef166f3a` | 2026-07-22 | ok |
| foundry | prereg_v18.json | `3e6e0c292` | `a7d0c2dd0` | 2026-07-22 | ok |
| foundry | prereg_v19.json | `559fe8559` | `aed436e19` | 2026-07-22 | ok |
| foundry | prereg_v20.json | `81445fbea` | `371d05efa` | 2026-07-22 | ok |
| foundry | prereg_v21.json | `ad53ff2b2` | `1880992fb` | 2026-07-22 | ok |
| foundry | prereg_v22.json | `cc8bc14c7` | `f4f4615ff` | 2026-07-22 | ok |
| foundry | prereg_v23.json | `3f207ca46` | `b773dab1c` | 2026-07-22 | ok |
| foundry | prereg_v24.json | `7daba39cc` | `e3262310b` | 2026-07-22 | ok |
| foundry | prereg_v25.json | `d67f9c1e3` | `e08ec34e9` | 2026-07-22 | ok |
| foundry | prereg_v26.json | `1579de278` | `7bf96e548` | 2026-07-22 | ok |
| foundry | prereg_v27.json | `f14cbdb4d` | `a63e21630` | 2026-07-22 | ok |
| foundry | prereg_v28.json | `5a16bb8d2` | `7491caa74` | 2026-07-22 | ok |
| foundry | prereg_v29.json | `43b4b4d13` | `6b3dba090` | 2026-07-23 | ok |
| foundry | prereg_v30.json | `004992bee` | `27e12e653` | 2026-07-23 | ok |
| foundry | prereg_v31.json | `d0de6cf09` | `19239d244` | 2026-07-23 | ok |
| foundry | prereg_v32.json | `5ffe82a64` | `d6e4ccd39` | 2026-07-23 | ok |
| foundry | prereg_v33.json | `9ba811f09` | `e6b8a1827` | 2026-07-23 | ok |
| proof-census | prereg_v1.json | `55c7df5ae` | `3581db30a` | 2026-07-20 | ok |
| desert-map | prereg_v1.json | `55c7df5ae` | `3581db30a` | 2026-07-20 | ok |

**43 sealed preregs; 43 resolve to a public commit, 0 pruned.**

## Native hardmap seals (post-migration)

Specs and preregs authored directly in `hardmap` — *after* the `uofa-lab` extraction —
were never in `uofa-lab`, so no old→new hash resolution applies: the seal **is** the
hardmap commit SHA that introduced the artifact, committed before any analysis ran
against it (`sealed-before-measured`).

| investigation | artifact | sealed (hardmap) | date | status |
|---|---|---|---|---|
| Quarry v1 | `eightfold/docs/specs/quarry-v1-row-expansion-spec.md` | `f74023ac4` | 2026-07-23 | ok — sealed before K1 analysis (spec sha256 `6fd3626b…`) |

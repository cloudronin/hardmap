# I-phase — dichotomy-oracle verification (N0)

Pins the exact theorem statements + scopes that the N1 Boolean-census oracles rely on. Web-verified
2026-07-21. **Discipline (spec kill/AGENTS §4): a column whose dichotomy fails verification drops to `open`;
a column whose dichotomy is verified but whose per-co-clone condition-check is not yet computed is filled where
determinate and left `open` elsewhere — never guessed.**

## Verified — fill as `derived`/`claimed` in N1

| Charge | Theorem | Statement (scope) | Per-co-clone rule |
|---|---|---|---|
| **decision** | **Schaefer 1978** | CSP(Γ) ∈ P if Γ is 0-valid, 1-valid, Horn, dual-Horn, bijunctive, or affine; else NP-complete. A **dichotomy**. | P for the six tractable classes; NPC otherwise. NPI is **empty** (prediction 1). |
| **counting** | **Creignou–Hermann 1996** | #CSP(Γ) ∈ FP if Γ is **affine**; else #P-complete. | FP iff affine; #P-complete otherwise (incl. Horn/dual-Horn/bijunctive/0-/1-valid). |
| **approximation** | **KSTW 2001** (+ Håstad 2001) | Max-CSP(Γ) ∈ PO if Γ is 0-valid, 1-valid, or 2-monotone; else APX-complete. Max-affine (Max-3LIN) is **inapprox** (Håstad). | PO for 0-/1-valid; inapprox for affine; APX-complete for Horn/dual-Horn/bijunctive/NP-hard. |
| **parallelization** | **ABISV 2009** (refining Schaefer via Post's lattice) | within-P classes: affine ∈ ⊕L ⊆ NC; bijunctive ∈ NL ⊆ NC; Horn/dual-Horn are **P-complete**; 0-/1-valid trivial ∈ NC. | NC for {affine, bijunctive, 0-valid, 1-valid}; P-complete for {Horn, dual-Horn}; **n.a.** for NPC (E2). |
| **localization** (I6) | **Barto–Kozik 2014** | bounded width iff Γ has two weak-NU polymorphisms of different arity; the **only** obstruction is affine/linear equations. Bounded width ⟹ CSP(Γ) ∈ P (in NL). | bounded-width for {0-/1-valid, Horn, dual-Horn, bijunctive}; **unbounded-width for affine** (the deceptive-terrain control) and for NP-hard. |

## Verified dichotomy EXISTS, per-co-clone check deferred → `open` in N1 v1

| Charge | Theorem | Why deferred |
|---|---|---|
| **parameterized** (I1) | **Marx 2005** — Boolean weighted-Sat (weight exactly k) is FPT or W[1]-complete (a parameterized Schaefer analog). | The tractable side is "weakly separable" Γ — a specific per-relation condition not yet computed per co-clone. Verified fillable; left `open` until the weakly-separable classifier is written (honest, not guessed). |
| **proof_size** (random) | **Molloy** (random-CSP resolution complexity) | About *random* Γ-instances (density-dialed), not the language directly; belongs with the N4 ensemble design (I5). `open` in v1. |

## Instrument columns — `measured` (N4), not this pass

`average_case`, `landscape` are filled by the Proof-Census apparatus on random Γ-ensembles (N4); `open` in v1.

## Roster (I2, R-B)

**Creignou–Kolaitis–Zanuttini 2008** (JCSS, "Structure identification of Boolean relations and plain bases for
co-clones") give a **plain basis per co-clone in Post's lattice, tabulated** — a set of relations generating
the co-clone with no auxiliary existential quantification (most are propositional-clause sets). This is the
roster-generator (R-B): instantiate one CKZ plain-basis representative per co-clone; the arity bound governs
reachable co-clones; enumeration of relation-sets (2^256 at arity 3) is never performed. Post's lattice is
countably infinite but its co-clones fall into finitely many named types (with infinite chains — e.g. the
S₀ᵏ/S₁ᵏ threshold families — that share a charge profile and are represented by their limit). N1 v1
implements the **named spine** (the ~dozen distinct-profile co-clones incl. the six Schaefer classes + the
registration anchors 2-SAT, 3-SAT, XOR-SAT, Horn-SAT, NAE-SAT, 1-in-3-SAT); finer/infinite-chain co-clones are
a documented v1.1 extension, never silently dropped.

## Prior-art (I4)

Survey-confidence re-check: the CSP-dichotomy program supplies the **columns** (per-language classifications
— Schaefer, Creignou–Hermann, KSTW, ABISV, Barto–Kozik, Marx), and CKZ organize the **rows** (co-clones + plain
bases). We are **not aware** of a prior artifact that assembles these into a single *cross-task charge table*
(languages × charges) with a null-model / factor analysis over it — that table is Foundry's contribution. This
"not aware of prior work" is the standing verdict; a deeper venue-grade search is a pre-submission task.

## Citations

Schaefer, STOC 1978 · Creignou & Hermann, Inf. Comput. 125 (1996) · Khanna–Sudan–Trevisan–Williamson, SICOMP
30 (2001); Håstad, JACM 48 (2001) · Allender–Bauland–Immerman–Schnoor–Vollmer, JCSS 75 (2009) · Barto & Kozik,
JACM 61 (2014) · Marx, Comput. Complexity 2005 · Creignou–Kolaitis–Zanuttini, JCSS 74 (2008).

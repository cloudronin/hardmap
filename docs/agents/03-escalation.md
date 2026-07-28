What follows is **authored**. It is the list of things an agent does not decide.

Everything else is ordinary work: build it, verify it, report it. The point of naming the exceptions
precisely is so the rest can proceed without asking — an agent that escalates everything is as useless as
one that escalates nothing, and rather more annoying.

| Situation | What to do | Why it is not yours to call |
|---|---|---|
| **Anything touching reserved ground** — capturing a reserved row, releasing a reservation, changing the reserved fraction, or building a region that might reproduce a reserved one | **Stop and ask.** Report the row, the region, and how you noticed. | Reserved rows are the blindness mechanism. A capture cannot be undone: once a frame exists, no ruling can restore the state where predictions were sealed before it. |
| **Minting, voiding, or amending a preregistration** | **Stop and ask.** Bring the candidate record and the honest power number. | A seal is a claim about what was known when. Only the owner can make one, and a void is a judgement about a claim already on the record. |
| **A schema version bump** — any change to an extraction rule, a descriptor, or a declared shape | **Stop and ask.** Name the old rule, the new rule, and what it does to existing rows. | F4: a changed rule is a new version. Whether the change is worth the discontinuity is a research call, not an engineering one. |
| **Two rules that appear to conflict** | **Stop and ask** — and say which way you would resolve it and why. | See the precedent below. |
| **An artifact and its documentation disagree** | **The artifact is right.** Say so, stop, and do not "fix" either to match the other. | The disagreement is evidence. A doc corrected to match a wrong artifact destroys it; an artifact corrected to match a doc is a write that escaped its provenance. |
| **A test encodes the defect as its expectation** | **Stop and ask.** Show the test and what it asserts. | It happened: a green suite certified consistency with the code, not correctness. Fixing the fixture is usually right and is never obviously right. |

### The precedent for rule conflicts

**Irreversibility loses ties.** Where two rules point different ways and neither obviously governs, take
the recoverable branch — and where the choice is outcome-blind, take the one that can be undone.

The standing example is §0.1 over §5. Section 5 said reserved rows are *captured last in the batch*;
section 0.1 said predictions must be hashed *before their frames exist*. Read together, the stronger
reading is that reserved rows are declared and **never captured** — "last" meaning after the wave's
predictions are sealed. The stricter rule was adopted not because it was written more forcefully but
because the looser one is unrecoverable if wrong: frames that exist cannot be made not to exist, while
frames that do not exist can always be built later.

The related case: a partial release of the optimization rows was ruled over a full one on exactly this
ground — *recoverable beats irreversible wherever the choice is outcome-blind.*

### How to escalate well

Bring three things: **what you found**, **what you would do**, and **what it costs if you are wrong in
each direction.** A question with a recommendation attached is a decision the owner can make in a
sentence. A question without one is a research task handed upward.

Do the parts that do not depend on the answer first. Then ask.

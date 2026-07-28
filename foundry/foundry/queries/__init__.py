"""The worked queries — ONE home, read by the CLI and rendered as documentation.

`QUERIES.md` in this package is the single source. `hardmap query --list` parses it, `hardmap query
<name>` executes the SQL out of it, and the file a reader browses on GitHub is the same file the runner
consumed. A separate machine-readable copy would be a second home for the same fact, and the two would
disagree the first time someone edited one.

IT LIVES INSIDE THE PACKAGE BECAUSE THE WHEEL MUST SHIP IT. Under `foundry/docs/` it was excluded from
the distribution, so a `pip install hardmap` user could not have run a named query even if the runner
existed. That is the same shape as the bug this whole unit exists to fix: the archive was reachable in
principle and not in fact.

THE OUTPUT BLOCKS ARE COMPILED, THE PROSE AND SQL ARE AUTHORED. Every output in the file was hand-pasted
once and then drifted: the file claimed "the output shown is from the current build" while showing a
frontier of 2 against an actual 16, and a candidate ledger of 344 against an actual 1942. Outputs are now
regenerated from the database by `foundry queries refresh`, which is the only way a worked example stays
worked.
"""

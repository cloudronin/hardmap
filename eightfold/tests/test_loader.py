"""Loader + the bundled pilot atlas must parse and validate clean."""
from eightfold import atlas, charges as C


def test_real_atlas_loads():
    entries = atlas.load_atlas()
    assert len(entries) >= 20
    ids = [e.problem_id for e in entries]
    assert len(ids) == len(set(ids))  # unique
    # decoupling witnesses present
    for w in ("vertex-cover", "clique", "permanent", "determinant", "xor-sat", "php"):
        assert w in ids


def test_real_atlas_validates_clean():
    entries = atlas.load_atlas()
    errs = atlas.validate_corpus(entries)
    assert errs == {}, errs


def test_roundtrip_serialization():
    entries = atlas.load_atlas()
    d = atlas.entry_to_dict(entries[0])
    again = atlas.entry_to_dict(atlas.entry_from_dict(d))
    assert again == d


def test_every_entry_has_all_charges():
    for e in atlas.load_atlas():
        assert sorted(c.charge for c in e.charges) == sorted(C.CHARGES)

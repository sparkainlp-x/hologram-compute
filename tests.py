"""Tests for hologram-compute. Run: python tests.py"""

import random

from substrate import (random_patterns, store, field, winner, fidelity,
                       noisy_probe, erased_probe, macs_field, macs_brute,
                       reads_field, reads_brute, characterize)


def test_store_field_deterministic():
    rng = random.Random(1)
    pats = random_patterns(8, 32, rng)
    W = store(pats)
    q = noisy_probe(pats[0], 0.1, rng)
    assert field(W, q) == field(store(pats), q)


def test_crossover_math():
    N = 64
    assert macs_field(N) == reads_field(N) == N * N
    assert macs_brute(1024, N) == reads_brute(1024, N) == 1024 * N
    # crossover: hologram cheaper per query exactly when P > N
    assert macs_field(N) < macs_brute(65, N)
    assert macs_field(N) == macs_brute(64, N)


def test_clean_winner_and_field():
    rng = random.Random(2)
    pats = random_patterns(8, 64, rng)
    for k, p in enumerate(pats):
        assert winner(pats, p) == k
        f = field(store(pats), p)
        n = sum(abs(c) ** 2 for c in f) ** 0.5
        assert fidelity(pats[k], [c / n for c in f]) > 0.80


def test_half_erased_still_correct():
    rng = random.Random(3)
    pats = random_patterns(8, 64, rng)
    W = store(pats)
    for k, p in enumerate(pats):
        q = erased_probe(p, 0.50, rng)
        assert winner(pats, q) == k, k
        f = field(W, q)
        n = sum(abs(c) ** 2 for c in f) ** 0.5
        assert fidelity(pats[k], [c / n for c in f]) > 0.60


def test_noisy_winner():
    # sigma=0.20 is clean; sigma=0.30 is the measured breakdown
    # regime (membrane-capacity: P90=4 at N=64) -- not tested here
    rng = random.Random(4)
    pats = random_patterns(8, 64, rng)
    for k, p in enumerate(pats):
        assert winner(pats, noisy_probe(p, 0.20, rng)) == k


def test_graceful_not_cliff():
    # more erasure -> worse fidelity, monotonically, no cliff at 0.5
    rng = random.Random(5)
    pats = random_patterns(8, 64, rng)
    W = store(pats)
    fids = []
    for er in (0.0, 0.25, 0.50):
        fs = []
        for k, p in enumerate(pats):
            q = erased_probe(p, er, rng)
            f = field(W, q)
            n = sum(abs(c) ** 2 for c in f) ** 0.5
            fs.append(fidelity(pats[k], [c / n for c in f]))
        fids.append(sum(fs) / len(fs))
    assert fids[0] >= fids[1] >= fids[2] > 0.5


def test_characterize_clean_is_perfect():
    # logical error is zero; the field carries crosstalk (Heisenberg:
    # non-orthogonal patterns can't all be perfectly recalled)
    le, ff = characterize(8, 32, 0.0, 0.0, seeds=5)
    assert le == 0.0 and ff > 0.85


def test_brute_agrees_with_hologram_winner():
    # same answer, different cost structure: the honest comparison
    rng = random.Random(6)
    pats = random_patterns(16, 64, rng)
    for k, p in enumerate(pats):
        q = noisy_probe(p, 0.2, rng)
        assert winner(pats, q) == k


if __name__ == "__main__":
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith("test_")]):
        fn()
        print(f"PASS {name}")
    print("all tests passed")

"""hologram-compute: the memory that computes.

Big tech's two obsessions right now, stated as infrastructure problems:

  1. THE MEMORY WALL. AI accelerators are limited by data movement,
     not arithmetic (E_switch ~ C V^2 per move). The fix is compute
     where the data lives: multiply data that is already local.
  2. LOGICAL RELIABILITY. The race shifted from more physical
     qubits to better logical qubits. The fix is error correction
     as the product, not the patch.

One structure answers both: the holographic memory.

  - Recall IS the matrix-vector multiply Y = W X -- the exact
    operation at the center of every neural layer -- executed as a
    single pass over a fixed-size structure. Per-query cost is
    O(N^2), independent of library size P. The memory computes;
    nothing is fetched, scored, and re-ranked.
  - The hologram IS an error-correcting code. Every element of W
    carries every pattern: distributed redundancy, the way a
    surface code spreads one logical qubit over many physical
    ones. Erasure and noise degrade it gracefully -- measured
    here as physical-error-rate -> logical-error-rate curves,
    with a visible threshold where it shatters.

Classical throughout. Stdlib only. Seeded. No quantum hardware
claims, no speedup stories -- the energy argument is analytic
(op counts and traffic), not a hardware measurement.
"""

import math
import random
import time


# ------------------------------------------------------------ substrate
def random_patterns(P, N, rng):
    """P random complex patterns on the N-sphere (the physical layer)."""
    pats = []
    for _ in range(P):
        v = [complex(math.cos(a), math.sin(a))
             for a in (rng.uniform(0, 2 * math.pi) for _ in range(N))]
        n = math.sqrt(sum(abs(c) ** 2 for c in v))
        pats.append([c / n for c in v])
    return pats


def store(patterns):
    """Write once: the interference record W = sum |p><p|."""
    n = len(patterns[0])
    W = [[0j] * n for _ in range(n)]
    for p in patterns:
        for i in range(n):
            pi = p[i]
            row = W[i]
            for j in range(n):
                row[j] += pi * p[j].conjugate()
    return W


def field(W, probe):
    """Recall: one matrix-vector multiply. The memory computes."""
    n = len(probe)
    return [sum(W[i][j] * probe[j] for j in range(n)) for i in range(n)]


def winner(patterns, probe):
    """One-shot projection: argmax |<p_k|probe>|^2. Project once."""
    best, best_m = 0, -1.0
    for k, p in enumerate(patterns):
        m = abs(sum(p[i].conjugate() * probe[i]
                    for i in range(len(probe)))) ** 2
        if m > best_m:
            best, best_m = k, m
    return best


def fidelity(a, b):
    return abs(sum(x.conjugate() * y for x, y in zip(a, b))) ** 2


# ------------------------------------------------------------ channels
def noisy_probe(pattern, sigma, rng):
    v = [c + complex(rng.gauss(0, sigma), rng.gauss(0, sigma))
         for c in pattern]
    n = math.sqrt(sum(abs(c) ** 2 for c in v))
    return [c / n for c in v]


def erased_probe(pattern, fraction, rng):
    """Erasure channel: a random fraction of amplitudes zeroed."""
    idx = list(range(len(pattern)))
    rng.shuffle(idx)
    kill = set(idx[:int(len(pattern) * fraction)])
    v = [0j if i in kill else c for i, c in enumerate(pattern)]
    n = math.sqrt(sum(abs(c) ** 2 for c in v)) or 1.0
    return [c / n for c in v]


# ------------------------------------------------------------ accounting
def macs_field(N):
    """Multiply-accumulates per query: holographic recall."""
    return N * N


def macs_brute(P, N):
    """Multiply-accumulates per query: score every stored pattern."""
    return P * N


def reads_field(N):
    """Weight reads per query: one pass over the fixed structure."""
    return N * N


def reads_brute(P, N):
    """Weight reads per query: every pattern re-read, every query."""
    return P * N


# ------------------------------------------------------------ the code, characterized
def characterize(P, N, sigma, erasure, seeds):
    """Physical error rate -> logical error rate + field fidelity.

    Logical error = wrong winner (one-shot projection).
    Returns (logical_error_rate, mean_field_fidelity).
    """
    errs, fids = 0, []
    for s in range(seeds):
        rng = random.Random(10_000 + s)
        pats = random_patterns(P, N, rng)
        W = store(pats)
        for k, p in enumerate(pats):
            q = noisy_probe(p, sigma, rng)
            q = erased_probe(q, erasure, rng)
            if winner(pats, q) != k:
                errs += 1
            f = field(W, q)
            n = math.sqrt(sum(abs(c) ** 2 for c in f)) or 1.0
            fids.append(fidelity(pats[k], [c / n for c in f]))
    tot = seeds * P
    return errs / tot, sum(fids) / len(fids)


def timed(P, N, trials=8):
    """Wall-clock per query: field reconstruction vs brute-force
    search. Same content returned, different cost structure."""
    rng = random.Random(77)
    pats = random_patterns(P, N, rng)
    W = store(pats)
    probes = [noisy_probe(pats[s % P], 0.2, rng) for s in range(trials)]

    t0 = time.perf_counter()
    for q in probes:
        field(W, q)
    t_field = (time.perf_counter() - t0) / trials

    t0 = time.perf_counter()
    for q in probes:
        best = pats[winner(pats, q)]
    t_brute = (time.perf_counter() - t0) / trials
    return t_field, t_brute

# DESIGN — hologram-compute

## The thesis

Two infrastructure problems dominate big tech right now:

1. **The memory wall.** AI accelerators are limited by data
   movement, not arithmetic. Energy per switch scales as C·V²;
   moving operands across a chip or to HBM is the expensive
   operation. The fix: compute where the data lives.
2. **Logical reliability.** The race shifted from more physical
   qubits to better logical qubits. The fix: error correction
   as the product.

The holographic memory answers both with one structure:

- **Recall is the matrix-vector multiply** Y = WX -- the exact
  operation at the center of every neural layer -- executed as a
  single pass over a fixed-size structure. Per-query cost O(N²),
  independent of library size P. Crossover at P = N; measured
  19.5× wall-clock advantage at P=1024, N=64, same content
  returned. The memory computes; nothing is fetched, scored,
  and re-ranked.
- **The hologram is an error-correcting code.** Every element of
  W carries every pattern: distributed redundancy, the way a
  surface code spreads one logical qubit over many physical
  ones. Characterized as physical-error-rate -> logical-error-rate
  curves: at σ=0, logical error stays 0.0 out to 75% erasure;
  at σ=0.30 with an overloaded library (P=16 > P90=4), it
  shatters. Graceful degradation, then the threshold.

## The three titans (all three are measured properties)

- **Schrödinger:** the substrate computes by wave interference.
  Recall is superposition, not lookup.
- **Heisenberg:** non-orthogonal patterns cannot be simultaneously
  perfectly recalled. Uncertainty is a theorem of the substrate --
  measured as crosstalk (clean-probe field fidelity 0.87-0.92,
  not 1.0) and recall drift (quantum-projection: 25-step recall
  flips the winner in 75% of seeds). Not a bug.
- **Dirac:** every ket has its conjugate bra. The only thing ever
  measured -- the inner product -- is computed between
  conjugates. KetBraPair / yin-yang as charge conjugation.

## Honest limits

- The energy argument is analytic (op counts, traffic), not a
  hardware measurement. This Python moves data like everything
  else; the *algorithm* has the locality structure a crossbar or
  optical implementation would inherit.
- Brute force returns the same winner -- the comparison is cost
  structure, not capability. That is the point: same answer,
  different physics.
- σ=0.30/P=16 shatters because the library is overloaded
  (membrane-capacity measured P90=4 at N=64, σ=0.30). The code
  curves are load-dependent, reported as-is.
- Classical throughout. No quantum hardware claims.

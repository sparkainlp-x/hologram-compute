# Hologram-Compute

**The memory that computes. The code that corrects.**

Big tech's two infrastructure problems -- the memory wall
(data movement, not arithmetic) and logical reliability
(better logical qubits, not more physical ones) -- answered
by one structure: the holographic memory.

- Recall **is** the matrix-vector multiply Y = WX, one pass over
  a fixed-size structure: O(N²) per query, independent of library
  size P. Measured 19.5× wall-clock vs brute-force search at
  P=1024, N=64 -- same content returned.
- The hologram **is** an error-correcting code: distributed
  redundancy characterized as physical-error-rate ->
  logical-error-rate curves. Zero logical errors out to 75%
  erasure at σ=0; an honest shatter threshold when overloaded.

Stdlib-only Python, seeded, AGPL-3.0. Classical throughout.

## Verified

- 8/8 tests pass
- Crossover at P = N, exact
- Graceful degradation under erasure, measured shatter under
  overload (consistent with membrane-capacity P90)

## Run it

```bash
python tests.py   # 8 tests
python demo.py    # crossover, wall-clock, code curves, titans
```

## Honest limits

Energy argument is analytic, not hardware-measured; brute force
finds the same winner (the comparison is cost structure);
code curves are load-dependent. Full account in `DESIGN.md`.

## Credits

Authors: Jean-François Brisson and Mun Seok Lee.
Lee, author of the Digital to Wave paradigm (Zenodo 21947036,
21947108), is the inspiration friend behind this wave and
membrane work. This package's code was built by Brisson with
AI assistance, except where a file already credits Lee as
author; the joint credit here is for the shared programme,
not a claim that Lee wrote every line of this package.

"""Demo: the memory that computes, the code that corrects.

1. The crossover: per-query MACs and weight reads, hologram vs
   brute-force search, as the library grows. The hologram's cost
   does not move with P.
2. Wall-clock at P=1024, N=64: same content, different structure.
3. The code, characterized: logical error rate and field fidelity
   vs erasure fraction and noise -- the threshold where it shatters.
4. The three titans.

Run: python demo.py
"""

from substrate import (characterize, timed, macs_field, macs_brute,
                       reads_field, reads_brute)


def main():
    N = 64
    print("== 1. the crossover: per-query cost vs library size P "
          f"(N={N}) ==")
    print(f"{'P':>6} {'MACs holo':>10} {'MACs brute':>11} "
          f"{'reads holo':>10} {'reads brute':>11}")
    for P in (16, 64, 256, 1024):
        print(f"{P:>6} {macs_field(N):>10} {macs_brute(P, N):>11} "
              f"{reads_field(N):>10} {reads_brute(P, N):>11}")
    print("crossover at P = N: past it, the hologram does less work\n"
          "per query, and its cost never moves with the library.\n")

    print("== 2. wall-clock per query, P=1024, N=64 ==")
    t_field, t_brute = timed(1024, 64)
    print(f"hologram field : {t_field * 1e3:7.2f} ms "
          f"({macs_field(N)} MACs)")
    print(f"brute-force    : {t_brute * 1e3:7.2f} ms "
          f"({macs_brute(1024, N)} MACs)")
    print(f"ratio          : {t_brute / t_field:7.2f}x "
          "(same content returned)\n")

    print("== 3. the code, characterized "
          "(P=16, N=64, 40 seeds) ==")
    print(f"{'sigma':>6} {'erasure':>8} {'logical err':>11} "
          f"{'field fidelity':>14}")
    for sigma in (0.0, 0.30):
        for er in (0.0, 0.25, 0.50, 0.75):
            le, ff = characterize(16, 64, sigma, er, seeds=40)
            print(f"{sigma:>6.2f} {er:>8.2f} {le:>11.4f} "
                  f"{ff:>14.4f}")
    print("no cliff: graceful degradation, then the shatter.\n")

    print("== 4. the three titans ==")
    print("Schrodinger: the substrate computes by wave interference.\n"
          "  Recall is superposition, not lookup.\n"
          "Heisenberg: non-orthogonal patterns cannot be simultaneously\n"
          "  perfectly recalled. Uncertainty is a theorem of the\n"
          "  substrate -- measured as crosstalk and recall drift,\n"
          "  not a bug in the code.\n"
          "Dirac: every ket has its conjugate bra. The only thing ever\n"
          "  measured -- the inner product -- is computed between\n"
          "  conjugates. Yin and yang as charge conjugation.\n")
    print("The future is not determined by imagination.\n"
          "It is determined by infrastructure.\n"
          "This is infrastructure: the memory that computes.")


if __name__ == "__main__":
    main()

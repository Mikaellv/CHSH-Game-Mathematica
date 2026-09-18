# CHSH Game — 3-Player Variant

Tools for exploring winning probabilities in a **3-player generalization of
the CHSH game**, a nonlocal game used to demonstrate that quantum
correlations (entanglement) let cooperating players win more often than any
strategy based on pre-shared classical randomness ("local hidden
variables") alone.

The repository has two independent pieces:

| File | What it does |
|---|---|
| `CHSH GAME SIMULATOR.py` | Monte-Carlo estimate of the winning probability of one specific **fixed, input-independent classical strategy**. |
| `CHSHgame_3players_calculations.nb` | Full symbolic/numeric **quantum-mechanical treatment**: builds a 3-qubit GHZ state, applies input-dependent projective measurements, derives a closed-form winning-probability function, and numerically maximizes it over the measurement settings. |

## The game

A referee privately and independently sends one random bit each to three
non-communicating players — `x` to Alice, `y` to Bob, `z` to Charlie (each
bit drawn uniformly from `{0, 1}`, so there are 8 equally likely input
triples). Each player replies with one bit, `a`, `b`, `c`. The players win
if their answers satisfy an AND-type condition on the inputs (the
GHZ/Mermin-style condition used in this notebook: they win when
`a ⊕ b ⊕ c` matches whether `x = y = z = 0`). The players may agree on a
strategy beforehand but cannot communicate once they receive their inputs.

- **Classical strategies** (players' answers are some pre-agreed function
  of their own input bit, possibly using shared randomness) are bounded by
  a fixed maximum winning probability.
- **Quantum strategies** (players share an entangled state and choose
  their measurement basis based on their input bit) can do better — this
  is the content of Bell/GHZ-type theorems.

The `CHSH-Game-Mathematica` notebook computes exactly how much better: it
optimizes over quantum measurement angles to find the maximum achievable
quantum winning probability, for comparison against classical strategies.

## `CHSH GAME SIMULATOR.py` (classical, Python)

This script does **not** implement a general classical (local-hidden-variable)
strategy. It fixes the players' output bits as constants — `a = 1`,
`b = 0`, `c = 0`, completely ignoring the input bits `x, y, z` — and simply
Monte-Carlo estimates the winning probability of *that one constant
strategy* over 10 000 random referee input triples. It's meant as a quick,
readable sanity check / starting point, not an optimal or adaptive
strategy search.

The header comments describe how the file began life as a simpler 2-player
version and was extended to 3 players (adding player C's bit `c` to the
output sum, and the `and zz` condition on Charlie's input). As checked into
this repository, both changes are already applied, so the file runs as a
3-player simulation out of the box.

### Requirements

Python 3.8+, standard library only (`random`) — no extra packages needed.

### Usage

```bash
python3 "CHSH GAME SIMULATOR.py"
```

Example output:

```
wins 0.8719
losses 0.1281
```

To try a different fixed strategy, edit the constants near the top of the
file:

```python
a = 1
b = 0
c = 0
```

Any combination of `0`/`1` values is a valid (if naive) classical strategy
to test — since none of `a, b, c` depend on the players' own input bits,
this only demonstrates one corner of the classical strategy space, not the
optimal classical bound.

## `CHSHgame_3players_calculations.nb` (quantum, Mathematica)

This notebook works out the actual quantum strategy and its winning
probability:

1. **State preparation** — the three players share the GHZ state
   `|ψ⟩ = (|000⟩ + |111⟩)/√2`.
2. **Measurement settings** — each player has two possible measurement
   bases (one per possible input bit), implemented as 2×2 rotation
   matrices parameterized by an angle: `A0/A1` (Alice, angle `x1`/`x2`),
   `B0/B1` (Bob, angle `y1`/`y2`), `C0/C1` (Charlie, angle `z1`/`z2`).
3. **Per-input winning probabilities** — for each of the 8 possible input
   triples `(x, y, z)`, the notebook works out the quantum-mechanical
   probability of each answer combination `(a, b, c)` that wins the game.
4. **Aggregate winning-probability function** `f(x1, x2, y1, y2, z1, z2)` —
   the average winning probability over all 8 (equally likely) input
   triples, as a closed-form trigonometric expression in the six
   measurement angles.
5. **Optimization** — `NMaximize` numerically searches over
   `x1, x2, y1, y2, z1, z2 ∈ [-π, π]` for the angles that maximize `f`,
   returning both the maximal winning probability and the optimal angles.

A saved run in the notebook finds a maximum winning probability of
`0.21875` at (numerically) `x1 ≈ 0`, `x2 ≈ π`, `y1 ≈ π`, `y2 ≈ -π`,
`z1 ≈ π`, `z2 ≈ -π` — re-running `NMaximize` may land on an equivalent
optimum reached via different (but physically equivalent) angles, since
the objective is periodic and highly symmetric.

### Requirements

- [Wolfram Mathematica](https://www.wolfram.com/mathematica/) or the free
  [Wolfram Engine](https://www.wolfram.com/engine/) (notebook created with
  Mathematica 13.1; no version-specific functions are used, so any
  reasonably recent version should work).

### Usage

1. Open `CHSHgame_3players_calculations.nb` in Mathematica (or the Wolfram
   Engine + a Jupyter kernel via the Wolfram Language kernel).
2. Evaluate the notebook top-to-bottom (**Evaluation → Evaluate Notebook**,
   or step through cell-by-cell to follow the derivation). Each stage is
   labeled with an inline `Text[...]` cell describing what it computes
   (e.g. *"Define our matrices"*, *"Winning pairs for input (0, 0, 0)"*,
   *"The probability of winning the game is:"*).
3. The final cells define `f[...]`, run `NMaximize`, and extract
   `max_value` and `optimal_values` (the winning probability and the
   angles that achieve it).

To explore a different variant of the game (e.g. a different winning
condition, or more/fewer players), edit the per-input winning-pair
expressions and rebuild `f` accordingly — the matrix/state-preparation
cells at the top of the notebook are reusable as-is.

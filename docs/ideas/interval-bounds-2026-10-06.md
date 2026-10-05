# Bounded reals carried through functions

An idea of Luciano's, 2026-10-06, from his note on what types are for in Luthier
(`sonolocalizacion/Lucianos ideas dir/funcion de los tipos en Luthier.txt`). Experimental: to be
picked up after the explicit generators, not before.

## The idea

`y = sin x` can be typed as a real, as a real in [-1, 1], or as `sin x` itself. The middle answer
is a type that can be carried through many functions (not all): if a function has a known bound
on every interval of its arguments, the bound of a complicated function comes out of the bounds
of its parts. Passing a value from the bounded type back to the plain one costs nothing; computing
the bound costs work at every operation. In return, a value carries a certificate of where it can
be, which is what a type is for (the principle of the note: a check made once is recorded in the
type, and never made again).

This is interval arithmetic (R. E. Moore, *Interval Analysis*, 1966), a case of abstract
interpretation (P. Cousot and R. Cousot, POPL 1977).

## The law

Notation: `X` is an interval `[lo, hi]` with `lo <= hi` (two `Float64` endpoints); `x` is a
`Float64` with `lo <= x <= hi`, written `x in X`; `f : Float64 -> Float64` is a function and
`F : Interval -> Interval` a function on intervals.

`F` is an *extension* of `f` when it encloses it:

    Encloses (f : Float64 -> Float64) (F : Interval -> Interval) (X : Interval) (x : In X) : Bool :=
      contains (F X) (f x)

where `contains Y y` is `Y.lo <= y and y <= Y.hi`. Every other fact follows from this one. If `F`
encloses `f` and `G` encloses `g`, then `G . F` encloses `g . f` (inclusion is preserved by
composition), so the extension of a composite is a corollary (`05` R10), not a law to certify
again. A bounded value is then the type

    In (X : Interval) : U := { x : Float64 | X.lo <= x and x <= X.hi }

and `f` applied to a value of `In X` is a value of `In (F X)`.

The law can be tested with no tolerance. The endpoints of `F X` are rounded outward, and whether
they enclose `f x` is decided in `Rational` through `toQ` (`lib/rational.lut`, `06 §8`), as the
rounding law of the doubles is.

## How it would fit the interpreter

Native code needs nothing new. Each primitive operation on `Float64` has an extension (`+`, `-`,
`*`, `/` with outward rounding; `exp`, `log`, `sqrt` monotone, evaluated at the endpoints; `sin`
and `cos` piecewise monotone, with their extrema checked for inclusion), so the machine can
evaluate the same term with intervals in place of doubles. The hard part is a branch: when `X`
straddles the condition of an `if`, both branches are evaluated and their results joined, which
loses precision.

An extern has no extension of its own. It declares one, `F : Interval -> Interval`, certified by
`Encloses`, or a Lipschitz bound from which one is built.

## Where it stops working

Some functions have no useful extension. A black box from numpy with no declared extension and no
Lipschitz bound cannot be carried.

The dependency problem is the real cost. Each occurrence of a variable is treated as independent,
so `x - x` over [-1, 1] gives [-2, 2] instead of 0. Over an expression with many occurrences, a
log-likelihood with 22 terms for instance, the naive bound grows until it says nothing.

The standard remedies, in increasing cost and precision:
- the mean value form `F(X) = f(c) + G(X) . (X - c)`, where `c` is the midpoint of `X` and `G` an
  extension of the gradient of `f`; its overestimation falls with the square of the width of `X`,
  and Luthier already certifies gradients (`IsGradient`, the score of a likelihood);
- affine arithmetic (J. L. D. Comba and J. Stolfi, 1993), which keeps first-order correlations
  between occurrences;
- Taylor models (M. Berz and K. Makino), a polynomial with an interval remainder.

Tools: ball arithmetic (a midpoint and a radius) in Arb by F. Johansson, now part of FLINT and
reachable from Python as `python-flint`; `mpmath.iv` for plain intervals.

## Uses in sonolocalización

1. Separation over a region. `distanceJacobian` asks that the measured pairs be apart
   (`SeparatedPairs`), and plan item 5.2 says a zero distance during the iterations cannot be
   certified ahead. With an extension of `pairDistance`, a box of positions whose lower bound of
   every measured distance is positive has no coincident nodes anywhere in it. The certificate
   would cover the region the fit moves in, not one point.
2. Tolerances computed instead of written. `scaledTol` and `roundingSlack` are constants today.
   With intervals or balls and directed rounding, the error bound of a computation comes out of
   the computation, which is what `06 §8` leaves open.
3. A global optimum. Branch and bound with intervals (E. Hansen, *Global Optimization Using
   Interval Analysis*) discards every box whose upper bound of the log-likelihood is below the
   best value found, and ends with a maximum certified global, not only stationary. With 30
   parameters it is expensive; this one is the experiment.

## Open questions

- Whether `Interval` is a type of `lib/` with its extensions as a theory (`Extension f`, a record
  with the law `Encloses`), or the machine's second mode of evaluation, or both.
- How a branch over an interval is typed: the join of the branches, or a split of the interval.
- Whether bounds belong in the type statically, when the endpoints are closed constants and the
  checker can compute them, or only at run time.

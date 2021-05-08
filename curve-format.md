.curve format
=============

This document explains the format of a `.curve` file used as input to
*describe-curve*. (The `.curve` filetype is optional but recommended.)

The general format is a list of `key: value` items, one on each line.
Blank lines and lines starting with `#` are ignored. The order of items
is not significant. The file is assumed to be encoded in UTF-8 (this only
matters for the `name` key, since all other keys only accept US-ASCII).

Keys
----

`name`
: The name of this curve. This has no effect on security checks but will
  be used in the output to refer to the curve.

`field`
: An integer expression giving the order of the base field. Integers are
  decimal unless prefixed with `0x` (hex) or `0b` (binary). `^`, `+`, and
  `-` can be used as binary operators. To specify an extension field use
  `p^m` (with parentheses around p if it is a nontrivial expression).

`curve`
: The curve equation in affine form. First spaces are removed and some other
  normalization (e.g. replacing coefficients with placeholders) is done.
  Then the result is matched against the supported curve equations.
  The variables `u` and `v`, x, and y can be used for coordinates; any other
  single-letter variable name or field element expression is assumed to be a
  parameter.

  The supported forms of curve equations are:
  * `y^2 = x^3 + a*x + b` (short Weierstrass)
  * `y^2 = x^3 + A*x^2 + B` (Montgomery)
  * `a*x^2 + y^2 = 1 + d*x^2*y^2` (twisted Edwards)

  If you specify a parameter in the curve equation, you do not also need to
  specify it in a separate item.

`<any single-letter variable name>`
: A field element expression giving the value of the parameter. Field element
  expressions can use `/` as a binary operator for division in the base field.

`generator`
: An optional specification of a point on the curve. This does not necessarily
  need to be in the large prime-order subgroup; if it is not then *describe-curve*
  will say so and give a point that is. The point is given as a pair of field
  element expressions `(x, y)` in affine coordinates. The special values `+ve`
  and `-ve` for a coordinate mean to infer that coordinate as the positive or
  negative square root implied by the other coordinate and the curve equation.

`construction`
: The name of a parameterized family of pairing-friendly curves. This typically
  includes an embedding degree, which can be omitted if there is only one
  possible embedding degree for a given family. For example:
  * `BN12` or `BN`;
  * `MNT<k>` for k in {2, 3, 4, 6};
  * `Freeman10` or `Freeman`;
  * `BLS<k>` for k in {12, 24};
  * `KSS<k>` for k in {8, 16, 18}.

  If this form of curve specification is used, then:
  * an integer parameter `u` must also be given;
  * `field` is optional, but if given it must be consistent with `u`;
  * the curve equation must match the construction.

There are examples of widely deployed curves in the `examples` directory.

If you have suggestions for extensions or improvements to this format, please
file an issue.

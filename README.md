What is this?
=============

*Describe-curve* is intended to be a utility for describing elliptic curves used in
cryptography. It is a work in progress and is *not yet ready for use*.
The [license](LICENSE) is MIT.

The plan is to make it usable as a Python/Sage library (for example to assert that
desired security properties of a given curve hold), or as a command-line program
that outputs a description of the curve.

The main focus will be on robust support for prime-order groups, e.g. Ristretto,
Decaf, or double-odd representations are recommended where applicable.

Unlike Safe Curves which is prescriptive, this software is descriptive: the idea is
that you can throw pretty much any purported elliptic curve at it, and it will tell
you what is up with that curve for cryptographic use — warts and all. Please read
the Philosophy section below as a guide to interpreting the output.

*Describe-curve* is a work in progress, but planned features include:

* Single-file, human-readable input format.
* Support for testing the "Safe Curves" criteria that are still relevant as of 2021.
* Output of provable-prime certificates.
* Support for pairing-friendly curves, including estimates of STNFS security.
* Support for detecting curve 2-cycles and describing both curves.
* Support for curves over extension fields with large prime characteristic.
* Recommendations of hash-to-curve and indistinguishable hash-from-curve methods.
* Support for j = 0 and j = 1728 curves, including finding isogenies for use in
  simplified SWU.
* Advice on coordinate formats and explicit formulae, if known.
* LaTeX or mdbook output format.

There are no plans to support:

* Obscure curve equations (anything other than short Weierstrass, Montgomery,
  and twisted Edwards).
* Curves over fields with small characteristic. (Don't use them.)
* Safe Curves criteria that are obsolete or irrelevant.
* Any form of curve generation (but if you want to use some of the tests as
  subroutines in your curve generation code, have at it!)

Prerequisites
-------------

Sage 9.2 or later is needed.

Usage
-----

Create a `.curve` file specifying your curve, following the format described
in [curve-format.md](curve-format.md). For example:

  name: Ed25519
  field: 2^255 - 19
  curve: -x^2 + y^2 = 1 + d*x^2*y^2
  d: -121665/121666
  generator: (+ve, 4/5)

or

  name: BLS12-381
  curve: y^2 = x^3 + 4
  construction: BLS12
  u: -15132376222941642752

There are more examples of widely deployed curves in the `curves` directory.

Given a curve specification in `mycurve.curve`, it can be processed using
`./describe-curve.sage mycurve.curve`. The default is to output in mdbook
format (with embedded LaTeX using `$...$` for math) to the file `mycurve.md`.

A file `mycurve.primes` will also be created to cache prime factorizations
used in the checking process; this greatly speeds up future runs. The usage
of this file is explained in [primes-format](primes-format.md).

Use `./describe-curve.sage --help` for more options.

Philosophy
----------

*describe-curve* is technically an [expert system](https://en.wikipedia.org/wiki/Expert_system),
of a kind that is long out-of-fashion in Artificial Intelligence circles.
Despite the relative lack of success of this kind of AI for more general
applications, it is well-suited to a problem domain in which the domain
knowledge is fairly easily encoded, but its application depends on heavy
computation.

One of the advantages of writing an expert system in a straightforward
procedural way is that the output can be fully explained in terms of the code.
That is, the code is a communication to experts of how the output (in this
case a curve description) is produced. Without this code and the ability
to review whether it is checking what is claimed, the output would be
valueless.

The domain knowledge that goes into the description, and the decisions about
what to say and what to leave out, are not and cannot be unbiased. On the
contrary, this is intended to be quite opinionated software, and the opinions
(modulo bugs) reflect my biases and preferences as a cryptographic engineer.
These are roughly in line with most of the cryptographic community (for the
curves that are supported), but nevertheless some controversies are to be
expected. The output will try to mention known controversies and to convey
uncertainties.

The output is intended for a somewhat cryptographically knowledgeable audience,
and does not attempt to avoid or define technical terms.

WARNING: even if this software were ready for use (which it is not), no
automated assessment can be a substitute for cryptographic expertise. In
particular, there is no claim that it would not be possible to produce curves
with security weaknesses and implementation pitfalls that *describe-curve*
does not detect, either accidentally, or (especially) deliberately. It is
intended to be used as a check on curves constructed in good faith by experts.

Contributing
------------

Contributions, bug reports, and feature requests are extremely welcome!
Please feel free to file issues and pull requests on this repo. Reports of
disagreement with the output on particular classes of curves are especially
valued.

Citation
--------

This software can be cited as:

Daira Hopwood and contributors. *describe-curve* software, version <...>.
https://github.com/daira/describe-curves

The version should be a release tag.

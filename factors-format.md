Usage of .factors files
=======================

The checking process involves creating Pocklington primality certificates,
which are stored in a `.factors` file.

The format of this file is a list of factorizations of the form
`factor(`<x>`): `<factorization>, where <x> is an integer and <factorization>
is a list of prime powers `p^m` separated by `*`.

It is possible to add factorizations manually, e.g. if a particular
factorization is too hard for Sage and needs to be done by external
factoring software. *describe-curve* will report factorizations that
are taking a long time.

If a `.factors` file is already present then it will be used to speed
up computations, but its contents will be checked. Please *do not*
assume that this checking is robust against adversarial input (even
though it is supposed to be). If in doubt, just delete the file and it
will be recreated.

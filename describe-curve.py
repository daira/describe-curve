#!/usr/bin/env -S sage -python

from sage.all import *
import sys
from os.path import splitext
from argparse import ArgumentParser

from formatting import FORMATTERS, FORMATTERS_HELP, infer_format, infer_output_filename
from output import output
from curve import Curve

VERSION = "0.1"


def main(args):
    parser = ArgumentParser(prog="./describe-curve.py", description="Describe an elliptic curve.")
    parser.add_argument("input", metavar="<input.curve>",
                        help="specify the input filename")
    parser.add_argument("--output", metavar="<outputfile>",
                        help="specify the output filename (default: input filename with filetype replaced according to format)")
    parser.add_argument("--format", choices=FORMATTERS.keys(),
                        help="specify the output format: " + FORMATTERS_HELP)
    parser.add_argument("--factors", metavar="<factorsfile>",
                        help="specify the file to be used for factorizations (default: input filename with filetype replaced by '.factors')")
    parser.add_argument("--no-primality-proofs", action="store_true", default=False,
                        help="don't prove primality; only use probable prime tests")
    parser.add_argument("--version", action="version", version="describe-curve " + VERSION)

    o = parser.parse_args(args or ["--help"])

    if o.format is None:
        o.format = infer_format(o.output)

    if o.output is None:
        o.output = infer_output_filename(o.input, o.format)

    if o.factors is None:
        o.factors = splitext(o.input)[0] + ".factors"

    print(o)
    try:
        with open(o.input, "r") as f:
            curvefile = f.read()
    except IOError as e:
        print("Could not read input file %r: %s" % (o.input, e))
        return 1

    curve = Curve(curvefile)
    curve.annotate()
    formatter = FORMATTERS[o.format]
    output(formatter(sys.stdout), curve)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env -S sage -python

from sage.all import *
import sys
from os.path import splitext
from argparse import ArgumentParser

from formatting import FORMATTERS, FORMAT_HELP, FORMATS_WITH_TITLES, infer_format, infer_output_filename
from output import output
from curve import Curve

VERSION = "0.1"


def error(e):
    print(str(e), file=sys.stderr)

def main(args):
    parser = ArgumentParser(prog="./describe-curve.py", description="Describe an elliptic curve.")
    parser.add_argument("inputs", nargs="+", metavar="<input.curve>",
                        help="specify the input filename(s)")
    parser.add_argument("--output", metavar="<outputfile>",
                        help="specify the output filename (default: input filename with filetype replaced according to format)")
    parser.add_argument("--format", choices=FORMATTERS.keys(),
                        help="specify the output format: " + FORMAT_HELP)
    parser.add_argument("--title", metavar="<title>",
                        help="specify the output title (only relevant for " + FORMATS_WITH_TITLES + ")")
    parser.add_argument("--factors", metavar="<factorsfile>",
                        help="specify the file to be used for factorizations (default: input filename with filetype replaced by '.factors')")
    parser.add_argument("--no-primality-proofs", action="store_true", default=False,
                        help="don't prove primality; only use probable prime tests")
    parser.add_argument("--traceback", action="store_true", default=False,
                        help="if an error occurs, show the exception traceback, and exit even if there are more input files")
    parser.add_argument("--version", action="version", version="describe-curve " + VERSION)

    o = parser.parse_args(args or ["--help"])

    if o.format is None:
        o.format = infer_format(o.output)

    if o.output is None and len(o.inputs) == 1:
        o.output = infer_output_filename(o.inputs[0], o.format)

    if o.output is None:
        error("No output file specified. Not inferring the output filename because there are multiple input files.")
        return 1

    if o.title is None:
        o.title = splitext(o.output)[0]

    print(o)
    with open(o.output, "w") as outfile:
        out = FORMATTERS[o.format](outfile)
        out.preamble(o.title)

        ret = 0
        for input in o.inputs:
            factors = o.factors or (splitext(input)[0] + ".factors")

            try:
                with open(input, "r") as f:
                    curvefile = f.read()
            except IOError as e:
                error("Could not read input file %r: %s" % (o.input, e))
                ret = 1
            else:
                try:
                    curve = Curve(curvefile)
                    curve.annotate(factors)
                    output(out, curve)
                except Exception as e:
                    if o.traceback: raise
                    error(e)
                    ret = 1

        out.postamble()

    return ret

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

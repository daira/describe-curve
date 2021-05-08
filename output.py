# Output an English description of the given curve properties.
# This should not include any nontrivial math.

def output(out, curve):
    out.preamble(curve.name)
    out.section(1, curve.name)
    out.para("{name} is a {kind}.".format(**curve.__dict__))
    out.postamble()

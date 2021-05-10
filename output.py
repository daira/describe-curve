# Output an English description of the given curve properties.
# This should not include any nontrivial math.

def output(out, curve):
    c = curve.__dict__
    out.section(1, curve.name)
    out.para("{name} is a {kind}.".format(**c))

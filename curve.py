# Parsing of the .curve format

class Curve:
    KEYS = {"source-url", "name", "field", "curve", "generator", "construction"}

    def __init__(self, curvefile):
        self.source_url = None
        self.name = None
        self.field = None
        self.curve = None
        self.generator = None
        self.construction = None
        self.parameters = dict()

        for line in curvefile.splitlines():
            if line.strip() == "":
                continue
            (key, sep, value) = line.partition(":")
            key = key.strip()
            if key.startswith("#"):
                continue
            if sep != ":":
                raise KeyError("Line does not contain ':' and is not blank or a comment line: " + line)

            value = value.strip()
            if len(key) == 1:
                self.parameters[key] = value
            elif key in self.KEYS:
                setattr(self, key.replace('-', '_'), value)
            else:
                raise KeyError("Unrecognized key name %r" % (key,))

        if self.name is None:
            raise KeyError("The 'name' key is required")
        if self.field is None and self.construction is None:
            raise KeyError("Either the 'field' or 'construction' key is required")
        if self.curve is None and self.construction is None:
            raise KeyError("Either the 'curve' or 'construction' key is required")

    def annotate(self):
        self.kind = "curve of unknown type"

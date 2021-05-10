# Formatting for Markdown, LaTeX, and HTML5

from os.path import splitext

class MarkdownFormatter(object):
    def __init__(self, writer):
        self.writer = writer

    def preamble(self, title):
        pass

    def postamble(self):
        pass

    def section(self, level, title):
        assert level >= 1 and level <= 5
        self.writer.write("%s %s\n\n" % ("#"*level, title))

    def para(self, content):
        self.writer.write(content + "\n\n")

    def displaymath(self, content):
        self.writer.write("\\[" + content + "\\]\n\n")

    def inlinemath(self, content):
        return "$" + content + "$"

    def link(self, anchor, url):
        return "[%s](%s)" % (anchor, url)

    def list(self, items):
        for item in items:
            self.writer.write("* " + item + "\n")

        self.writer.write("\n")


class LaTeXFormatter(object):
    SECTION_COMMANDS = ["section", "subsection", "subsubsection", "paragraph", "subparagraph"]

    def __init__(self, writer):
        self.writer = writer

    def preamble(self, title):
        self.writer.write("\\documentclass{article}\n")
        self.writer.write("\\usepackage{amsmath,amssymb,amsfonts}\n")
        self.writer.write("\\usepackage{hyperref}\n")
        self.writer.write("\hypersetup{\n"
                          "  pdfborderstyle={/S/U/W 0.7},\n"
                          "  pdfinfo={Title={%s}}\n"
                          "}\n" % (title,))
        self.writer.write("\\begin{document}\n\n")

    def postamble(self):
        self.writer.write("\\end{document}\n")

    def section(self, level, title):
        assert level >= 1 and level <= 5
        self.writer.write("\\%s{%s}\n\n" % (self.SECTION_COMMANDS[level-1], title))

    def para(self, content):
        self.writer.write(content + "\n\n")

    def displaymath(self, content):
        self.writer.write("\\[" + content + "\\]\n\n")

    def inlinemath(self, content):
        return "$" + content + "$"

    def link(self, anchor, url):
        return "\\href{%s}{%s}" % (url, anchor)

    def list(self, items):
        self.writer.write("\\begin{itemize}\n")
        for item in items:
            self.writer.write("  \\item " + item + "\n")

        self.writer.write("\\end{itemize}\n\n")


class HTML5Formatter(object):
    def __init__(self, writer):
        self.writer = writer

    def preamble(self, title):
        # <https://katex.org/docs/autorender.html>
        self.writer.write((
            '<!DOCTYPE html>\n'
            '<html>\n'
            '<head>\n'
            '  <meta charset="utf-8" />\n'
            '  <title>%s</title>\n'
            '  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.9/dist/katex.min.css" integrity="sha384-r/BYDnh2ViiCwqZt5VJVWuADDic3NnnTIEOv4hOh05nSfB6tjWpKmn1kUHOVkMXc" crossorigin="anonymous">\n'
            '  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.13.9/dist/katex.min.js" integrity="sha384-zDIgORxjImEWftZXZpWLs2l57fMX9B3yWFPN5Ecabe211Hm5ZG/OIz2b07DYPUcH" crossorigin="anonymous"></script>\n'
            '  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.13.9/dist/contrib/auto-render.min.js" integrity="sha384-vZTG03m+2yp6N6BNi5iM4rW4oIwk5DfcNdFfxkk9ZWpDriOkXX8voJBFrAO7MpVl" crossorigin="anonymous"></script>\n'
            '  <script>\n'
            '    document.addEventListener("DOMContentLoaded", function() {\n'
            '      renderMathInElement(document.body, {\n'
            '        delimiters: [\n'
            '          {left: "$", right: "$", display: true},\n'
            '          {left: "\\[", right: "\\]", display: true}\n'
            '        ],\n'
            '        throwOnError: true\n'
            '      });\n'
            '    });\n'
            '  </script>\n'
            '</head>\n'
            '<body>\n'
            ) % (title,))

    def postamble(self):
        self.writer.write("</body>\n")
        self.writer.write("</html>\n")

    def section(self, level, title):
        assert level >= 1 and level <= 5
        self.writer.write("  <h%d>%s</h%d>\n" % (level, title, level))

    def para(self, content):
        self.writer.write("  <p>" + content + "</p>\n")

    def displaymath(self, content):
        self.writer.write("  <p>\\[" + content + "\\]</p>\n")

    def inlinemath(self, content):
        return "$" + content + "$"

    def link(self, anchor, url):
        return '<a href="%s">%s</a>' % (url, anchor)

    def list(self, items):
        self.writer.write("  <ul>\n")
        for item in items:
            self.writer.write("    <li>" + item + "</li>\n")

        self.writer.write("  </ul>\n")


FORMATTERS = {
    "md": MarkdownFormatter,
    "latex": LaTeXFormatter,
    "html": HTML5Formatter,
}

FORMAT_HELP = "Markdown, LaTeX, or HTML5 (default: md)"
FORMATS_WITH_TITLES = "LaTeX and HTML5"

def infer_format(output_filename):
    if output_filename is None:
        return "md"

    format = splitext(output_filename)[1][1:]
    if format == "tex":
        return "latex"
    if format not in FORMATTERS:
        return "md"

    return format

def infer_output_filename(input_filename, format):
    if format == "latex":
        format = "tex"

    return splitext(input_filename)[0] + "." + format

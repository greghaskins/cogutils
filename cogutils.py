"""Utility functions for use in cog scripts. 

Requires: 
cog: http://pypi.python.org/pypi/cogapp
Optional:
pygments: http://pygments.org/
"""

def include(filename, start=None, end=None):
    """Include the text of an external file verbatim."""
    import cog
    with open(filename, 'r') as f:
        text = f.read()
    text = _subset_lines(text, start, end)
    cog.outl(text)
    
def Includer(prefix="", suffix=""):
    """Wraps the include function by prepending and appending fixed text to
    its output."""
    def _include(*args, **kwargs):
        import cog
        cog.out(prefix)
        include(*args, **kwargs)
        cog.out(suffix)
    return _include

def include_with_syntax(filename, start=None, end=None, lexer=None):
    """Includes the text of an external file, highlighting with pygments."""
    import pygments
    import pygments.lexers
    import cog
    
    with open(filename, 'r') as f:
        text = f.read()
        
    if lexer is None:
        lexer = pygments.lexers.guess_lexer_for_filename(filename, text)
    elif isinstance(lexer, basestring):
        lexer = pygments.lexers.get_lexer_by_name(lexer)

    formatter = get_syntax_formatter()
    text = _subset_lines(text, start, end)
    
    cog.out(pygments.highlight(text, lexer, formatter))

def set_syntax_formatter(formatter=None):
    """Sets or determines the appropriate syntax formatter for this file."""
    import pygments.formatters
    import cog
    if formatter is None:
        formatter = pygments.formatters.get_formatter_for_filename(cog.outFile)
    elif isinstance(formatter, basestring):
        formatter = pygments.formatters.get_formatter_by_name(formatter)
    cog.pygments_formatter = formatter
    return formatter

def get_syntax_formatter():
    """Returns the pygments syntax formatter, if one is set."""
    import cog
    try:
        return cog.pygments_formatter
    except AttributeError:
        raise RuntimeError("no formatter set. call set_syntax_formatter() "
                           "first")
    
def print_syntax_styles():
    """Print the style definitions for the formatter. Note that this does NOT
    include the wrapping <style> tag."""
    import cog
    formatter = get_syntax_formatter()
    cog.out(formatter.get_style_defs())
    
def _subset_lines(text, start=None, end=None):
    """Utility function returning only lines between the given start and end
    line numbers (inclusive)."""
    if start or end:
        lines = text.split('\n')
        start = 1 if start is None else start
        end = len(lines) + 1 if end is None else end
        text = '\n'.join(lines[start-1:end])
    return text
        
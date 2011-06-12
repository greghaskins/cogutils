# `cogutils`: Utility functions for text processing with Cog #

`cogutils` is a small module that provides a few handy, reusable functions for
scripting with [Cog](http://nedbatchelder.com/code/cog/).

## Basic file inclusion ##

### `cogutils.include(filename, start=None, end=None)` ###

Writing documentation it's often annoying to have code samples inline, so
the `include()` function may be used to keep them in a separate (up-to-date)
file and have the text (or selected lines from it) included by Cog. Think of
it as the Cog version of a CPP `#include` statement.

For example, including a code snippet in a GitHub readme file:
```
<!--[[[cog
	import cog
	import cogutils
	cog.outl("``` python \n")
	cogutils.include("source_file.py")
	cog.outl("```")
]]]-->
# source will get inserted here
<!--[[[end]]]-->
```

Note that `start` and `end` are inclusive and indexed by one (so they 
correspond with the line numbers in your editor).

### `cogutils.Includer(prefix="", suffix="")` ###

Alternatively, you could use `cogutils.Includer` to return a callable which 
prepends a prefix and/or suffix each time:

```
<!--[[[cog
	import cog
	import cogutils
	py_block = cogutils.Includer(prefix="``` python \n", suffix="```")
	py_block("source_file.py")
]]]-->
# source will get inserted here, wrapped in the same fenced block style
<!--[[[end]]]-->
```

The benefit of this method is that you can re-use the same callable later on 
in the file (for instance, if you had several code blocks that needed the same
fencepost-style wrapping). [DRY](http://en.wikipedia.org/wiki/Don't_repeat_yourself)
[FTW](http://en.wiktionary.org/wiki/for_the_win).


## Syntax-highlighted file inclusion ##

`cogutils` also provides a way to run included files through the 
[pygments](http://pygments.org) syntax highlighter prior to being included
inline.

### `set_syntax_formatter(formatter=None)` ###

Sets the pygments formatter to be used (e.g. 'html', 'latex'). `formatter`
may be either a `pygments.formatter.Formatter` instance, or the name of some
formatter that can be found by 
`pygments.formatters.get_formatter_by_name(formatter)`.
This function must be called before `include_with_syntax(..)`, otherwise it 
would not know which output format to use.

### `include_with_syntax(filename, start=None, end=None, lexer=None)` ##

Similar to `cogutils.include(..)`, but uses pygments to return the highlighted
version of the included text. `lexer` may be either a `pygments.lexer.Lexer`
instance, the name of some lexer that can be found by 
`pygments.lexers.get_lexer_by_name(lexer)`, or `None`, in which case the lexer
will be guessed based on the filename.

### `print_syntax_styles()` ###

Inserts the syntax formatter style definitions, for use e.g. inside a `<style>`
tag at the beginning of the file.

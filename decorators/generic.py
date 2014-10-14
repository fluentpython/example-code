r"""
htmlize(): generic function example

# BEGIN HTMLIZE_DEMO

>>> htmlize({1, 2, 3})  # <1>
'<pre>{1, 2, 3}</pre>'
>>> htmlize(abs)
'<pre>&lt;built-in function abs&gt;</pre>'
>>> htmlize('Heimlich & Co.\n- a game')  # <2>
'<p>Heimlich &amp; Co.<br>\n- a game</p>'
>>> htmlize(42)  # <3>
'<pre>42 (0x2a)</pre>'
>>> print(htmlize(['alpha', 66, {3, 2, 1}]))  # <4>
<ul>
<li><p>alpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>

# END HTMLIZE_DEMO
"""

# BEGIN HTMLIZE

from functools import singledispatch
import html

@singledispatch  # <1>
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

@htmlize.register(str)  # <2>
def _(text):            # <3>
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)

@htmlize.register(int)  # <4>
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)

@htmlize.register(list)
def _(a_list):
    inner = '</li>\n<li>'.join(htmlize(item) for item in a_list)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

# END HTMLIZE


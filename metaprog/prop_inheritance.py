"""
Alex Martelli, _Python in a Nutshell, 2e._ (O'Reilly, 2006), p. 101

==========================
Properties and inheritance
==========================

Properties are inherited normally, just like any other attribute.
However, there’s a little trap for the unwary: the methods called
upon to access a property are those that are defined in the class
in which the property itself is defined, without intrinsic use of
further overriding that may happen in subclasses. For example:
"""

class B(object):

    def f(self):
        return 23

    g = property(f)

class C(B):

    def f(self):
        return 42

c = C()

print(c.g) # prints 23, not 42

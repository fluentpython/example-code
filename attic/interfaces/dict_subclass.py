# Code and text by BitBucket user "enigmacurry" posted to
# https://bitbucket.org/pypy/pypy/issue/708/discrepancy-in-dict-subclass-__getitem__
# Adapted by Luciano Ramalho:
# - changed comments to docstring to run with doctest;
# - added test for Test class raising exception
# - and added () to print.

"""
This is a test case to describe a bug I'm seeing in PyPy 1.5. I have
a Cache object that is a dictionary that supports lookup via regular
attribute access. For instance:

    >>> c = Cache()
    >>> c["asdf"] = "asdf"
    >>> c.asdf == c["asdf"]
    True
    >>> t = Test()
    >>> t["asdf"] = "asdf"
    >>> t.asdf == t["asdf"]
    Traceback (most recent call last):
      ...
    Exception: Trying to getitem: asdf

When looking up keys via attribute, PyPy 1.5 calls __getitem__
whereas CPython 2.7.1 does not.
"""

class Cache(dict):
    "A dictionary that supports attribute style key lookup"
    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__ = self

class Test(Cache):
    def __getitem__(self, item):
        # I want to process items differently than attributes:
        raise Exception("Trying to getitem: %s" % item)

if __name__ == "__main__":
    t = Test()
    t["asdf"] = "asdf"
    #CPython does not call __getitem__ .. PyPy does:
    print(t.asdf)
    #Doesn't matter if it's a member of __dict__ or not:
    print(t.__getattribute__)

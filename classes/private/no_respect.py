
"""
In the Jython registry file there is this line:

python.security.respectJavaAccessibility = true

Set this to false and Jython provides access to non-public
fields, methods, and constructors of Java objects.
"""

import Confidential

message = Confidential('top secret text')
for name in dir(message):
    attr = getattr(message, name)
    if not callable(attr):  # non-methods only
        print name + '\t=', attr

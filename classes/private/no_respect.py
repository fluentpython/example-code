# In the Jython registry:
# python.security.respectJavaAccessibility = false
# Setting this to false will allow Jython to provide access to
# non-public fields, methods, and constructors of Java objects.

import Confidential

message = Confidential("text you shoudn't see")
for name in dir(message):
    attr = getattr(message, name)
    if not callable(attr):  # ignore methods
        print name, '=', attr

from java.lang.reflect import Modifier
import Confidential

message = Confidential('top secret text')
fields = Confidential.getDeclaredFields()
for field in fields:
    # list private fields only
    if Modifier.isPrivate(field.getModifiers()):
        field.setAccessible(True) # break the lock
        print 'field:', field
        print '\t', field.getName(), '=', field.get(message)

import Confidential

message = Confidential("text you shoudn't see")
private_field = Confidential.getDeclaredField('secret')
private_field.setAccessible(True)  # break the lock!
print 'message.secret =', private_field.get(message)

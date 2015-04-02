# BEGIN REGISTRATION_ABRIDGED
registry = []

def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

print('running main()')
print('registry ->', registry)
f1()
# END REGISTRATION_ABRIDGED

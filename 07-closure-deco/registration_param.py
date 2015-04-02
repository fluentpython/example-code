# BEGIN REGISTRATION_PARAM

registry = set()  # <1>

def register(active=True):  # <2>
    def decorate(func):  # <3>
        print('running register(active=%s)->decorate(%s)'
              % (active, func))
        if active:   # <4>
            registry.add(func)
        else:
            registry.discard(func)  # <5>

        return func  # <6>
    return decorate  # <7>

@register(active=False)  # <8>
def f1():
    print('running f1()')

@register()  # <9>
def f2():
    print('running f2()')

def f3():
    print('running f3()')

# END REGISTRATION_PARAM

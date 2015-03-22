def deco_alpha(func):
    print('<<100>> deco_alpha')

    def inner_alpha():
        print('<<200>> deco_alpha')
        func()

    return inner_alpha


def deco_beta(cls):
    print('<<300>> deco_beta')

    def inner_beta(self):
        print('<<400>> inner_beta')
        print("result from 'deco_beta::inner_beta'")

    cls.method3 = inner_beta
    return cls


print('<<500>> evaldecos mudule body')

>>> def f1(a):
...     print(a)
...     print(b)
...
>>> f1(3)
3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in f1
NameError: name 'b' is not defined
>>> b = 6
>>> f1(3)
3
6

>>> def f2(a):
...     print(a)
...     print(b)
...     b = 9
...
>>> f2(3)
3
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in f2
UnboundLocalError: local variable 'b' referenced before assignment


# BEGIN F1_DIS
>>> from dis import dis
>>> dis(f1)
  2           0 LOAD_GLOBAL              0 (print)  <1>
              3 LOAD_FAST                0 (a)  <2>
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 POP_TOP

  3          10 LOAD_GLOBAL              0 (print)
             13 LOAD_GLOBAL              1 (b)  <3>
             16 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             19 POP_TOP
             20 LOAD_CONST               0 (None)
             23 RETURN_VALUE
# END F1_DIS
# BEGIN F2_DIS
>>> dis(f2)
  2           0 LOAD_GLOBAL              0 (print)
              3 LOAD_FAST                0 (a)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 POP_TOP

  3          10 LOAD_GLOBAL              0 (print)
             13 LOAD_FAST                1 (b)  <1>
             16 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             19 POP_TOP

  4          20 LOAD_CONST               1 (9)
             23 STORE_FAST               1 (b)
             26 LOAD_CONST               0 (None)
             29 RETURN_VALUE
# END F2_DIS
>>> def f3(a):
...     global b
...     print(a)
...     print(b)
...     b = 9
...
>>> f3(3)
3
6
>>> b
9
# BEGIN F3_DIS
>>> dis(f3)
  3           0 LOAD_GLOBAL              0 (print)
              3 LOAD_FAST                0 (a)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 POP_TOP

  4          10 LOAD_GLOBAL              0 (print)
             13 LOAD_GLOBAL              1 (b)
             16 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             19 POP_TOP

  5          20 LOAD_CONST               1 (9)
             23 STORE_GLOBAL             1 (b)
             26 LOAD_CONST               0 (None)
             29 RETURN_VALUE
# END F3_DIS

>>> def f4(b):
...     def f5(a):
...         nonlocal b
...         print(a)
...         print(b)
...         b = 7
...     return f5
...
>>> f5 = f4(8)
>>> f5(2)
2
8
>>> b
9
>>> f5(3)
3
7????

>>> dis(f5)
  4           0 LOAD_GLOBAL              0 (print)
              3 LOAD_FAST                0 (a)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 POP_TOP

  5          10 LOAD_GLOBAL              0 (print)
             13 LOAD_DEREF               0 (b)
             16 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             19 POP_TOP

  6          20 LOAD_CONST               1 (7)
             23 STORE_DEREF              0 (b)
             26 LOAD_CONST               0 (None)
             29 RETURN_VALUE



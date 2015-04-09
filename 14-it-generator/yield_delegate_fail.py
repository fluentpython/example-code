""" Example from `Python: The Full Monty`__ -- A Tested Semantics for the
Python Programming Language

__ http://cs.brown.edu/~sk/Publications/Papers/Published/pmmwplck-python-full-monty/

"The following program, [...] seems to perform a simple abstraction over the
process of yielding:"

Citation:

Joe Gibbs Politz, Alejandro Martinez, Matthew Milano, Sumner Warren,
Daniel Patterson, Junsong Li, Anand Chitipothu, and Shriram Krishnamurthi.
2013. Python: the full monty. SIGPLAN Not. 48, 10 (October 2013), 217-232.
DOI=10.1145/2544173.2509536 http://doi.acm.org/10.1145/2544173.2509536
"""

# BEGIN YIELD_DELEGATE_FAIL
def f():
    def do_yield(n):
        yield n
    x = 0
    while True:
        x += 1
        do_yield(x)
# END YIELD_DELEGATE_FAIL

if __name__ == '__main__':
    print('Invoking f() results in an infinite loop')
    f()

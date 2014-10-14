==============
Tombola tests
==============

Every concrete subclass of Tombola should pass these tests.


Create and load instance from iterable::

	>>> balls = list(range(3))
	>>> globe = TombolaUnderTest(balls)
	>>> globe.loaded()
	True


Pop and collect balls::

	>>> picks = []
	>>> picks.append(globe.pop())
	>>> picks.append(globe.pop())
	>>> picks.append(globe.pop())


Check state and results::

	>>> globe.loaded()
	False
	>>> sorted(picks) == balls
	True


Reload::

	>>> globe.load(balls)
	>>> globe.loaded()
	True
	>>> picks = [globe.pop() for i in balls]
	>>> globe.loaded()
	False


Load and pop 20 balls to verify that the order has changed::

	>>> balls = list(range(20))
	>>> globe = TombolaUnderTest(balls)
	>>> picks = []
	>>> while globe.loaded():
	...     picks.append(globe.pop())
	>>> len(picks) == len(balls)
	True
	>>> picks != balls
	True


Also check that the order is not simply reversed either::

	>>> picks[::-1] != balls
	True

Note: last 2 tests each have 1 chance in 20! (factorial) of failing even if the implementation is OK. 1/20!, or approximately 4.11e-19, is the probability of the 20 balls coming out, by chance, in the exact order the were loaded.

Check that `LookupError` (or a subclass) is the exception thrown when the device is empty::

	>>> globe = TombolaUnderTest([])
	>>> try:
	...     globe.pop()
	... except LookupError as exc:
	...     print('OK')
	OK


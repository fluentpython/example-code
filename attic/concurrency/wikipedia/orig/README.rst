=====================================
Wikipedia Picture of the Day examples
=====================================

These examples use various asynchronous programming techniques to download 
images and metadata from the English Wikipedia `Picture of the Day`_ archive.

.. _Picture of the Day: http://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day/Archive


--------
Timings
--------

``sync.py``
===========

::

    $ time python sync.py 2014-06 -q 5
    5 images downloaded (167.8 Kbytes total)

    real    0m6.272s
    user    0m0.065s
    sys 0m0.039s

    $ time python sync.py 2014-06 -q 5
    5 images downloaded (167.8 Kbytes total)

    real    0m5.447s
    user    0m0.068s
    sys 0m0.040s

    $ time python sync.py 2014-06 -q 5
    5 images downloaded (167.8 Kbytes total)

    real    0m6.314s
    user    0m0.068s
    sys 0m0.040s

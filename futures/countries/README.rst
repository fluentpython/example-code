====================================
Configuring a local test environment
====================================

tl;dr;
======

This text explains how to configure **nginx** and **vaurien** to build a local
mirror of the data to run the flag download examples while avoiding network
traffic and introducing controlled delays and errors for testing, thanks to
the **vaurien** proxy.


Rationale and overview
======================

The flag download examples are designed to compare the performance of
different approaches to finding and downloading files from the Web. However,
we don't want to hit a public server with multiple requests per second while
testing, and we want to be able to simulate high latency and random network
errors.

For this setup I chose **nginx** as the HTTP server because it is very fast
and easy to configure, and the **vaurien** proxy because it was designed by
Mozilla to introduce delays and network errors for testing.

The archive ``flags.zip``, contains a directory ``flags/`` with 194
subdirectories, each containing a ``.gif` image and a ``metadata.json`` file.
These images are public-domain flags copied from the CIA World Fact Book [1].

[1] https://www.cia.gov/library/publications/the-world-factbook/

Once these files are unpacked to the ``flags/`` directory and **nginx** is
configured, you can experiment with the ``flags*.py``examples without hitting
the network.


Instructions
============

1. Unpack test data
-------------------

Unpack the initial data in the ``countries/`` directory and verify that 194
directories are created in ``countries/flags/``, each with a ``.gif`` and
a ``metadata.json`` file::

    $ unzip flags.zip
    ... many lines omitted...
       creating: flags/zw/
      inflating: flags/zw/metadata.json
      inflating: flags/zw/zw.gif
    $ ls flags | wc -w
    194
    $ find flags | grep .gif | wc -l
    194
    $ find flags | grep .json | wc -l
    194
    $ ls flags/ad
    ad.gif      metadata.json


2. Install **nginx**
--------------------

Download and install **nginx**. I used version 1.6.2 -- the latest
stable version as I write this.

- Download page: http://nginx.org/en/download.html

- Beginner's guide: http://nginx.org/en/docs/beginners_guide.html


3. Configure **nginx**
----------------------

Edit the the ``nginx.conf`` file to set the port and document root. 
You can determine which ``nginx.conf`` is in use by running::

    $ nginx -V

The output starts with::

    nginx version: nginx/1.6.2
    built by clang 6.0 (clang-600.0.51) (based on LLVM 3.5svn)
    TLS SNI support enabled
    configure arguments:...

Among the configure arguments you'll see ``--conf-path=``. That's the
file you will edit.

Most of the content in ``nginx.conf`` is within a block labeled ``http``
and enclosed in curly braces. Within that block there can be multiple
blocks labeled ``server``. Add another ``server`` block like this one::

    server {
        listen       8001;

        location /flags/ {
            root   /full-path-to.../countries/;
        }
    }

After editing ``nginx.conf`` the server must be started (if it's not
running) or told to reload the configuration file::

    $ nginx  # to start, if necessary
    $ nginx -s reload  # to reload the configuration

To test the configuration, open the URL below in a browser. You should
see the blue, yellow and red flag of Andorra::

    http://localhost:8001/flags/ad/ad.gif

If the test fails, please double check the procedure just described and
refer to the **nginx** documentation.

At this point you may run the ``flags_*2.py`` examples against the **nginx**
install by changing the ``BASE_URL`` constant in ``flags_sequential2.py``.
However, **nginx** is so fast that you will not see much difference in run
time between the sequential and the threaded versions, for example. For more
realistic testing with simulated network lag, we need **vaurien**.


4. Install and run **vaurien**
------------------------------

**vaurien depends on gevent which is only available for Python 2.5-2.7. To
install vaurien I opened another shell, created another ``virtualenv`` for
Python 2.7, and used that environment to install and run vaurien::

    $ virtualenv-2.7 .env27 --no-site-packages --distribute
    New python executable in .env27/bin/python
    Installing setuptools, pip...done.
    $ . .env27/bin/activate
    (.env27)$ pip install vaurien
    Downloading/unpacking vaurien
      Downloading vaurien-1.9.tar.gz (50kB): 50kB downloaded
    ...many lines and a few minutes later...

    Successfully installed vaurien cornice gevent statsd-client vaurienclient
    greenlet http-parser pyramid simplejson requests zope.interface
    translationstring PasteDeploy WebOb repoze.lru zope.deprecation venusian
    Cleaning up...
    (.env27)$

Using that same shell with the ``.env27`` activated, run the ``vaurien_delay.sh`` script in the ``countries/`` directory::

    (.env27)$ $ ./vaurien_delay.sh
    2015-02-25 20:20:17 [69124] [INFO] Starting the Chaos TCP Server
    2015-02-25 20:20:17 [69124] [INFO] Options:
    2015-02-25 20:20:17 [69124] [INFO] * proxies from localhost:8002 to localhost:8001
    2015-02-25 20:20:17 [69124] [INFO] * timeout: 30
    2015-02-25 20:20:17 [69124] [INFO] * stay_connected: 0
    2015-02-25 20:20:17 [69124] [INFO] * pool_max_size: 100
    2015-02-25 20:20:17 [69124] [INFO] * pool_timeout: 30
    2015-02-25 20:20:17 [69124] [INFO] * async_mode: 1

The ``vaurien_delay.sh`` adds a 1s delay to every response.

There is also the ``vaurien_error_delay.sh`` script which produces errors in 25% of the responses and a .5 se delay to 50% of the responses.


Platform-specific instructions
==============================

Nginx setup on Mac OS X
-----------------------

Homebrew (copy & paste code at the bottom of http://brew.sh/)::

  $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  $ brew doctor
  $ brew install nginx

Download and unpack::

Docroot is: /usr/local/var/www
/usr/local/etc/nginx/nginx.conf

To have launchd start nginx at login:
    ln -sfv /usr/local/opt/nginx/*.plist ~/Library/LaunchAgents
Then to load nginx now:
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.nginx.plist
Or, if you don't want/need launchctl, you can just run:
    nginx



Nginx setup on Lubuntu 14.04.1 LTS
----------------------------------

Docroot is: /usr/share/nginx/html


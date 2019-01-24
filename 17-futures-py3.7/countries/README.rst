============================
Setting up Nginx and Vaurien
============================

This text explains how to configure Nginx and Vaurien to test HTTP client code while avoiding network traffic and introducing simulated delays and errors. This setup is necessary if you want to experiment with the ``flags2*.py`` image download examples in this directory -- covered in chapters 17 and 18 of Fluent Python.


Overview
========

The flag download examples are designed to compare the performance of different approaches to finding and downloading files from the Web. However, we don't want to hit a public server with multiple requests per second while testing, and we want to be able to simulate high latency and random network errors.

For this setup I chose Nginx as the HTTP server because it is very fast and easy to configure, and Toxiproxy — designed by Shopify to introduce delays and network errors for testing distributed systems.

The archive ``flags.zip``, contains a directory ``flags/`` with 194 subdirectories, each containing a ``.gif`` image and a ``metadata.json`` file. These are public-domain images copied from the `CIA World Fact Book <https://www.cia.gov/library/publications/the-world-factbook/>`_.

Once these files are unpacked to the ``flags/`` directory and Nginx is configured, you can experiment with the ``flags2*.py`` examples without hitting the network.


Procedure
=========

1. Unpack test data
-------------------

The instructions in this section are for GNU/Linux or OSX using the command line. Windows users should have no difficulty doing the same operations with the Windows Exporer GUI.

Unpack the initial data in the ``fancy_flags/`` directory::

  $ unzip flags.zip
  ... many lines omitted ...
     creating: flags/zw/
    inflating: flags/zw/metadata.json
    inflating: flags/zw/zw.gif


Verify that 194 directories are created in ``fancy_flags/flags/``, each with a ``.gif`` and a ``metadata.json`` file::


  $ ls flags | wc -w
  194
  $ find flags | grep .gif | wc -l
  194
  $ find flags | grep .json | wc -l
  194
  $ ls flags/ad
  ad.gif      metadata.json


2. Install Nginx
----------------

Download and install Nginx. I used version 1.6.2 -- the latest stable version as I write this.

* Download page: http://nginx.org/en/download.html

* Beginner's guide: http://nginx.org/en/docs/beginners_guide.html


3. Configure Nginx
------------------

Edit the the ``nginx.conf`` file to set the port and document root. You can determine which ``nginx.conf`` is in use by running::


  $ nginx -V


The output starts with::

  nginx version: nginx/1.6.2
  built by clang 6.0 (clang-600.0.51) (based on LLVM 3.5svn)
  TLS SNI support enabled
  configure arguments:...


Among the configure arguments you'll see ``--conf-path=``. That's the file you will edit.

Most of the content in ``nginx.conf`` is within a block labeled ``http`` and enclosed in curly braces. Within that block there can be multiple blocks labeled ``server``. Add another ``server`` block like this one::


  server {
      listen       8001;

      location /flags/ {
          root   /full-path-to.../countries/;
      }
  }


After editing ``nginx.conf`` the server must be started (if it's not running) or told to reload the configuration file::


  $ nginx  # to start, if necessary
  $ nginx -s reload  # to reload the configuration


To test the configuration, open the URL http://localhost:8001/flags/ad/ad.gif in a browser. You should see the blue, yellow and red flag of Andorra.

If the test fails, please double check the procedure just described and refer to the Nginx documentation.

At this point you may run the ``flags_*2.py`` examples against the Nginx install by providing the ``--server LOCAL`` command line option. For example::


  $ python3 flags2_threadpool.py -s LOCAL
  LOCAL site: http://localhost:8001/flags
  Searching for 20 flags: from BD to VN
  20 concurrent connections will be used.
  --------------------
  20 flags downloaded.
  Elapsed time: 0.09s


Note that Nginx is so fast that you will not see much difference in run time between the sequential and the concurrent versions. For more realistic testing with simulated network lag, we need to set up Toxiproxy.


4. Install and run Toxiproxy
----------------------------

Install...

In one terminal:

  $ toxiproxy-server

In another terminal:

  $ toxiproxy-cli create nginx_flags_delay -l localhost:8002 -u localhost:8001
  Created new proxy nginx_flags_delay
  $ toxiproxy-cli toxic add nginx_flags_delay -t latency -a latency=500
  Added downstream latency toxic 'latency_downstream' on proxy 'nginx_flags_delay'


This creates an HTTP proxy on port 8002 which adds a 0.5s delay to every response. You can test it with a browser on port 8002: http://localhost:8002/flags/ad/ad.gif -- the flag of Andorra should appear after ½ second.

TODO: UPDATE NEXT PARAGRAPH

There is also the ``XXX`` script which runs a proxy on port 8003 producing errors in 25% of the responses and a .5 s delay to 50% of the responses. You can also test it with the browser on port 8003, but rememeber that errors are expected.


Platform-specific instructions
==============================


Nginx setup on Mac OS X
------------------------

Homebrew (copy & paste code at the bottom of http://brew.sh/)::


  $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  $ brew doctor
  $ brew install nginx


Download and unpack::

Docroot is: /usr/local/var/www
/usr/local/etc/nginx/nginx.conf


::

  To have launchd start nginx at login:
      ln -sfv /usr/local/opt/nginx/*.plist ~/Library/LaunchAgents
  Then to load nginx now:
      launchctl load ~/Library/LaunchAgents/homebrew.mxcl.nginx.plist
  Or, if you don't want/need launchctl, you can just run:
      nginx



Nginx setup on Lubuntu 14.04.1 LTS
----------------------------------

Docroot is: /usr/share/nginx/html



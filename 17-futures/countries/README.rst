============================
Setting up Nginx and Vaurien
============================

This text explains how to configure Nginx and Vaurien to test HTTP client code while avoiding network traffic and introducing simulated delays and errors. This setup is necessary if you want to experiment with the ``flags2*.py`` image download examples in this directory -- covered in chapters 17 and 18 of Fluent Python.


Overview
========

The flag download examples are designed to compare the performance of different approaches to finding and downloading files from the Web. However, we don't want to hit a public server with multiple requests per second while testing, and we want to be able to simulate high latency and random network errors.

For this setup I chose Nginx as the HTTP server because it is very fast and easy to configure, and the Vaurien proxy because it was designed by Mozilla to introduce delays and network errors for testing Web services.

The archive ``flags.zip``, contains a directory ``flags/`` with 194 subdirectories, each containing a ``.gif`` image and a ``metadata.json`` file. These are public-domain images copied from the `CIA World Fact Book <https://www.cia.gov/library/publications/the-world-factbook/>`_.

Once these files are unpacked to the ``flags/`` directory and Nginx is configured, you can experiment with the ``flags2*.py`` examples without hitting the network.


Procedure
=========

1. Install Docker_.
.. _Docker: https://docs.docker.com/engine/installation/
2. run:

    $ ./docker_run_servers.sh

4: access http://localhot:8001 to acess nginx with no delay
5: access http://localhot:8002 to acess nginx with delay
6: access http://localhot:8003 to acess nginx with delay and errors

You can use this address to check Chapter 18 example of downloading flags

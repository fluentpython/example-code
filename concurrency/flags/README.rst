=========================================
Setting up the test environment 
=========================================

Some of the concurrency examples in this book require a local HTTP
server. These instructions show how I setup Ngnix on GNU/Linux,
Mac OS X 10.9 and Windows 7.

Nginx setup on Mac OS X
========================

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
==================================

/usr/share/nginx/html

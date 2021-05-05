#! /bin/bash

set -eux

sudo apt-get install -y python-pip python-dev libpq-dev postgresql postgresql-contrib nginx


sudo apt install -y gunicorn

sudo cp scripts/gunicorn.conf /etc/init/gunicorn.conf
sudo service gunicorn restart
sudo service gunicorn status


sudo apt-get install -y nginx

sudo rm -f /var/log/nginx/access.log
sudo rm -f /var/log/nginx/error.log

sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-available/default

sudo cp scripts/nginx.conf /etc/nginx/sites-available/default
sudo cp scripts/nginx.conf /etc/nginx/sites-enabled/default

sudo service nginx restart
sudo service nginx status

#!/bin/bash

# Function to switch profiles
switch_profile() {
  if [ "$PROFILE" == "drupal" ]; then
    cp /etc/drupal/httpd.conf /usr/local/apache2/conf/httpd.conf
    cp /etc/drupal/modsecurity.conf /usr/local/apache2/conf/modsecurity.conf
    cp /etc/drupal/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf
    cp -r /etc/drupal/web/* /var/www/html/
  elif [ "$PROFILE" == "wordpress" ]; then
    cp /etc/wordpress/httpd.conf /usr/local/apache2/conf/httpd.conf
    cp /etc/wordpress/modsecurity.conf /usr/local/apache2/conf/modsecurity.conf
    cp /etc/wordpress/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf
    cp -r /etc/wordpress/web/* /var/www/html/
  else
    echo "Unknown PROFILE: $PROFILE"
    exit 1
  fi
}

# Initial profile setup
switch_profile

# Start Apache in the foreground
exec httpd-foreground
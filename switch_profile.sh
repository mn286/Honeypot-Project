#!/bin/bash

PROFILE=$1

# Function to switch profiles
switch_profile() {
  echo "Switching to profile: $PROFILE"

  # Switch profiles by copying the correct configuration files
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
    echo "Unknown profile: $PROFILE"
    exit 1
  fi

  # Start Apache server
  echo "Starting Apache server..."
  apachectl restart

  # Check if Apache started correctly
  if [ $? -ne 0 ]; then
    echo "Failed to start Apache."
    exit 1
  fi

  echo "Profile switched to $PROFILE and Apache restarted successfully."
}

# Execute the function to switch profiles
switch_profile

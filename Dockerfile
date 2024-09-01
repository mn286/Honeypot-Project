FROM owasp/modsecurity-crs:apache

USER root

# Install necessary packages
RUN apt-get update && apt-get install -y git php libapache2-mod-php php-mysql php-gd php-xml php-mbstring apache2-utils

# Download OWASP CRS
RUN git clone https://github.com/coreruleset/coreruleset.git /usr/local/modsecurity-crs

# Find and set the correct path for the PHP module
RUN PHP_MODULE=$(find /usr/lib/apache2/modules -name 'libphp*.so') && \
    if [ -n "$PHP_MODULE" ]; then \
        cp $PHP_MODULE /usr/local/apache2/modules/ && \
        echo "LoadModule php_module modules/$(basename $PHP_MODULE)" >> /etc/apache2/php-module.conf; \
    else \
        echo "PHP module not found"; \
        exit 1; \
    fi

# Copy profile-specific configurations
COPY drupal/ /etc/drupal/
COPY wordpress/ /etc/wordpress/

# Copy the default ModSecurity CRS setup
RUN cp /usr/local/modsecurity-crs/crs-setup.conf.example /usr/local/modsecurity-crs/crs-setup.conf

# Enable necessary Apache modules
RUN a2enmod rewrite unique_id

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copying the switch_profile.sh script into the container
COPY switch_profile.sh /usr/local/bin/switch_profile.sh

# Giving the script execute permissions
RUN chmod +x /usr/local/bin/switch_profile.sh


# Expose port 80
EXPOSE 80

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

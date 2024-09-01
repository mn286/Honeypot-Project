<?php
/**
 * @file
 * Drupal's primary configuration file.
 */

$databases = array (
  'default' => 
  array (
    'default' => 
    array (
      'database' => 'drupal',
      'username' => 'root',
      'password' => '',
      'host' => 'localhost',
      'port' => '',
      'driver' => 'mysql',
      'prefix' => '',
    ),
  ),
);

$settings['hash_salt'] = 'random-hash-value';

$config_directories['sync'] = 'sites/default/files/config_HASH';
?>

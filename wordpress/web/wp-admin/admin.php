<?php
// Set WordPress-like headers
header("X-Powered-By: WordPress");
header("X-Content-Type-Options: nosniff");
header("X-Frame-Options: SAMEORIGIN");
header("X-WP-Cache: MISS");

// Output an empty HTML page that appears to be a WordPress admin page to bots
echo "<!-- This is a honeypot WordPress admin page -->";
exit;
?>

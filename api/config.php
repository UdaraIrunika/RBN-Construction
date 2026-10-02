<?php
/**
 * Form handler configuration.
 * Values are read from environment variables first (set them in cPanel or
 * the server config). Never commit real addresses or passwords to Git.
 */
declare(strict_types=1);

if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'config.php') {
    http_response_code(404);
    exit;
}

return [
    // Where enquiries are delivered
    'mail_to'      => getenv('RBN_MAIL_TO')   ?: 'replace-me@yourdomain.lk',
    // Must be an address on your own domain (prevents spoofing / spam flags)
    'mail_from'    => getenv('RBN_MAIL_FROM') ?: 'website@yourdomain.lk',
    'site_name'    => 'R.B.N. Construction website',
    // Rate limit: max submissions per IP per window
    'rate_max'     => 5,
    'rate_window'  => 600, // seconds
    // Reject forms submitted faster than this (bots)
    'min_seconds'  => 3,
    // Folder for rate-limit files — keep it OUTSIDE the public web root
    'storage_dir'  => getenv('RBN_STORAGE_DIR') ?: sys_get_temp_dir() . '/rbn-forms',
];

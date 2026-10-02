<?php
/**
 * Issues a per-session CSRF token for the website forms.
 * GET /api/token.php  →  {"token": "..."}
 */
declare(strict_types=1);

require __DIR__ . '/bootstrap.php';

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    json_out(405, ['ok' => false, 'message' => 'Method not allowed.']);
}

if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

header('Cache-Control: no-store');
json_out(200, ['token' => $_SESSION['csrf_token']]);

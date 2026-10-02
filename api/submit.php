<?php
/**
 * Handles contact, quote and careers form submissions.
 * Protections: same-origin check, CSRF token, honeypot, minimum fill time,
 * per-IP rate limiting, strict whitelist validation, header-injection safe mail.
 *
 * Production tip: replace mail() with authenticated SMTP (e.g. PHPMailer)
 * using credentials from environment variables, for reliable delivery.
 */
declare(strict_types=1);

require __DIR__ . '/bootstrap.php';
$config = require __DIR__ . '/config.php';

/* ---------- 1. Method & origin ---------- */
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    json_out(405, ['ok' => false, 'message' => 'Method not allowed.']);
}

$host   = $_SERVER['HTTP_HOST'] ?? '';
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($origin !== '' && parse_url($origin, PHP_URL_HOST) !== parse_url('//' . $host, PHP_URL_HOST)) {
    json_out(403, ['ok' => false, 'message' => 'The request could not be verified.']);
}

/* ---------- 2. CSRF ---------- */
$token = (string)($_POST['csrf_token'] ?? '');
if (empty($_SESSION['csrf_token']) || !hash_equals($_SESSION['csrf_token'], $token)) {
    json_out(403, ['ok' => false, 'message' => 'Your session expired. Reload the page and try again.']);
}

/* ---------- 3. Bot checks (silent success so bots learn nothing) ---------- */
$started = (int)($_POST['form_started'] ?? 0);
if (($_POST['website'] ?? '') !== '' || ($started > 0 && time() - $started < $config['min_seconds'])) {
    json_out(200, ['ok' => true]);
}

/* ---------- 4. Rate limit per IP ---------- */
function rate_limited(array $config): bool
{
    $dir = $config['storage_dir'];
    if (!is_dir($dir) && !@mkdir($dir, 0700, true)) {
        return false; // fail open on storage error, but log it
    }
    $ip   = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $file = $dir . '/' . hash('sha256', $ip) . '.json';
    $now  = time();
    $hits = [];
    $fh = @fopen($file, 'c+');
    if (!$fh) return false;
    flock($fh, LOCK_EX);
    $raw  = stream_get_contents($fh);
    $hits = array_values(array_filter(json_decode($raw ?: '[]', true) ?: [], fn($t) => is_int($t) && $t > $now - $config['rate_window']));
    $limited = count($hits) >= $config['rate_max'];
    if (!$limited) {
        $hits[] = $now;
        ftruncate($fh, 0);
        rewind($fh);
        fwrite($fh, json_encode($hits));
    }
    flock($fh, LOCK_UN);
    fclose($fh);
    return $limited;
}

if (rate_limited($config)) {
    json_out(429, ['ok' => false, 'message' => 'Too many messages from this connection. Wait a few minutes and try again.']);
}

/* ---------- 5. Validation (whitelist per form) ---------- */
$forms = [
    'contact' => ['name' => [true, 100], 'phone' => [true, 20], 'email' => [false, 150], 'message' => [true, 2000]],
    'career'  => ['name' => [true, 100], 'phone' => [true, 20], 'email' => [false, 150], 'role' => [true, 80], 'message' => [true, 2000]],
    'quote'   => [
        'project_type' => [true, 30], 'location' => [true, 150], 'floors' => [false, 3], 'floor_area' => [false, 7],
        'budget' => [false, 40], 'start' => [true, 40], 'drawings' => [true, 40], 'details' => [false, 3000],
        'name' => [true, 100], 'phone' => [true, 20], 'email' => [false, 150], 'contact_pref' => [false, 20],
    ],
];
$type = (string)($_POST['form_type'] ?? '');
if (!isset($forms[$type])) {
    json_out(400, ['ok' => false, 'message' => 'Unknown form.']);
}

$clean  = [];
$errors = [];
foreach ($forms[$type] as $field => [$required, $max]) {
    $value = trim((string)($_POST[$field] ?? ''));
    $value = preg_replace('/[^\P{C}\n\t]/u', '', $value) ?? ''; // strip control chars except newline/tab
    if ($required && $value === '') { $errors[] = $field; continue; }
    if (mb_strlen($value) > $max)   { $errors[] = $field; continue; }
    $clean[$field] = $value;
}

if (($clean['email'] ?? '') !== '' && !filter_var($clean['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'email';
if (isset($clean['phone']) && !preg_match('/^[0-9 +()\-]{9,20}$/', $clean['phone']))     $errors[] = 'phone';
foreach (['floors', 'floor_area'] as $n) {
    if (($clean[$n] ?? '') !== '' && !ctype_digit($clean[$n])) $errors[] = $n;
}
$allowedTypes = ['residential', 'commercial', 'renovation', 'civil', 'maintenance', 'other'];
if ($type === 'quote' && !in_array($clean['project_type'] ?? '', $allowedTypes, true)) $errors[] = 'project_type';

if ($errors) {
    json_out(422, ['ok' => false, 'message' => 'Some fields need attention.', 'fields' => array_values(array_unique($errors))]);
}

/* ---------- 6. Send ---------- */
$labels = ['contact' => 'Contact message', 'career' => 'Job application', 'quote' => 'Quote request'];
$subject = sprintf('[%s] %s from %s', $config['site_name'], $labels[$type], $clean['name']);
$subject = '=?UTF-8?B?' . base64_encode(str_replace(["\r", "\n"], ' ', $subject)) . '?=';

$body = $labels[$type] . "\n" . str_repeat('=', 40) . "\n\n";
foreach ($clean as $k => $v) {
    $body .= str_pad(ucwords(str_replace('_', ' ', $k)) . ':', 16) . ($v === '' ? '-' : $v) . "\n";
}
$body .= "\nSubmitted: " . date('Y-m-d H:i:s') . "\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

$headers = [
    'From: ' . $config['site_name'] . ' <' . $config['mail_from'] . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: RBN-Website',
];
if (($clean['email'] ?? '') !== '') {
    $headers[] = 'Reply-To: ' . $clean['email']; // validated above, cannot contain CR/LF
}

$sent = @mail($config['mail_to'], $subject, $body, implode("\r\n", $headers), '-f' . $config['mail_from']);
if (!$sent) {
    error_log('[rbn-forms] mail() failed for form type ' . $type);
    json_out(500, ['ok' => false, 'message' => 'The message could not be sent.']);
}

// Rotate the token after a successful submission
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));
json_out(200, ['ok' => true]);

#!/usr/bin/env php
<?php
require __DIR__ . '/vendor/autoload.php';

use BrowscapPHP\Browscap;

$browscap = new Browscap();
$stdin = fopen('php://stdin', 'r');

$start = microtime(True);
while (($line = fgets($stdin)) !== False) {
  $ua = rtrim($line);
  $match = $browscap->getBrowser($ua);
  echo $match->browser_name_regex, "\n";
}
$duration = (microtime(True) - $start);

fclose($stdin);

fwrite(STDERR, "Total duration = $duration sec\n");

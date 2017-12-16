user_agents.txt: the top 4000 unique user agents that accessed
https://whatismyip.com.br in November, 2017.

Requirements
============

- PHP composer

.. code-block:: bash
  
  composer install
  # Either use the provided browscap.ini file (instructions below)
  # or download the latest from http://browscap.org/stream?q=Full_PHP_BrowsCapINI
  xzcat browscap.ini.xz >vendor/browscap/browscap-php/resources/browscap.ini
  # Create the cache
  vendor/bin/browscap-php browscap:convert
  # Run the comparison and the md5 sums should match
  make
  # To measure the durations again
  make clean compare

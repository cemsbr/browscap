#!/bin/bash
# Analyze code and upload results to SonarQube
coverage run --source=browscap setup.py test
coverage xml -i
nosetests --with-xunit
pylint browscap -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --disable=C0111,C0103 >pylint-report.txt
sonar-scanner

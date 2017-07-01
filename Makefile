SRC=browscapy

help:
	@echo 'Usage:'
	@echo '  make tests:    Run tests.'
	@echo '  make coverage: Run tests and display test coverage.'
	@echo '  make lint:     Run several linters.'

env:
	@export PYTHONPATH="$$PWD:$$PYTHONPATH"

.PHONY: tests
tests: env
	@python setup.py test

auto-tests:
	while [ True ]; do \
		if make coverage; then \
		    notify-send -t 3 -u low 'Tests Passed  :)'; \
		else \
			notify-send -t 3 -u critical 'Tests Failed  :('; \
		fi; \
		sleep 1; \
		inotifywait -re modify ${SRC}/ tests/; \
	done

coverage:
	@coverage run setup.py test
	@coverage report

lint:
	@echo Pylama
	@echo ======
	pylama ${SRC} tests
	@echo
	@echo RSTcheck
	@echo ========
	find . -type f -name "*.rst" | xargs rstcheck
	@echo
	@echo 'Vulture (unused code)'
	@echo '====================='
	vulture ${SRC}
	@echo
	@echo 'Bandit (vulnerabilities)'
	@echo '========================'
	bandit -r ${SRC}
	@echo
	@echo Safety
	@echo ======
	safety check
	@echo
	@echo 'Eradicate (commented-out code)'
	@echo '=============================='
	eradicate -r ${SRC} tests

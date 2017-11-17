SRC=browscapy

help:
	@echo 'Usage:'
	@echo '  make tests:       Run tests.'
	@echo '  make auto-tests:  Run tests when files are modified and display notification.'
	@echo '  make coverage:    Run tests and display test coverage.'
	@echo '  make lint:        Run several linters.'

clean:
	python setup.py clean
	rm -rf .eggs/ .tox/ build/ dist/ browscapy.egg-info/

auto-tests:
	while [ True ]; do \
		if make coverage; then \
			notify-send -t 3 -u low 'Tests Passed  :)'; \
		else \
			notify-send -t 3 -u critical 'Tests Failed  :('; \
		fi; \
		sleep 1; \
		inotifywait -re modify --format="%f" --exclude=".*\.swp" ${SRC}/ tests/; \
	done

coverage:
	@coverage run setup.py test
	@coverage report

mypy:
	mypy --disallow-any-unimported --disallow-any-expr --disallow-any-decorated --disallow-any-explicit --disallow-any-generics --disallow-subclassing-any --warn-return-any browscapy tests

lint:
	@echo mypy
	@echo ====
	mypy --disallow-any-unimported --disallow-any-expr --disallow-any-decorated --disallow-any-explicit --disallow-any-generics --disallow-subclassing-any --warn-return-any ${SRC} tests
	@echo "\nyala"
	@echo ====
	yala ${SRC} tests
#	@echo
#	@echo RSTcheck
#	@echo ========
#	find . -type f -name "*.rst" | xargs rstcheck
#	@echo
#	@echo 'Vulture (unused code)'
#	@echo '====================='
#	vulture ${SRC}
#	@echo
#	@echo 'Bandit (vulnerabilities)'
#	@echo '========================'
#	bandit -r ${SRC}
#	@echo
#	@echo Safety
#	@echo ======
#	safety check
#	@echo
#	@echo 'Eradicate (commented-out code)'
#	@echo '=============================='
#	eradicate -r ${SRC} tests

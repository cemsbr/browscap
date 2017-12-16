compare: python.out.txt php.out.txt
	@md5sum *.out.txt

python.out.txt: user_agents.txt.bz2
	@echo -n 'Python: '
	@bzcat user_agents.txt.bz2 | head -n 200 | ./search.py | ./normalize.py >python.out.txt

php.out.txt: user_agents.txt.bz2
	@echo -n '   PHP: '
	@bzcat user_agents.txt.bz2 | head -n 200 | ./search.php >php.out.txt

clean:
	rm -f python.out.txt php.out.txt

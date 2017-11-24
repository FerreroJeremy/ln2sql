clean:
	rm -rf *.json *.pyc
test:
	python3 -m unittest tests/test_*
	rm -rf *.json *.pyc
clean:
	rm -rf *.json *.pyc
test:
	python3 -m unittest tests/test_unit
	rm -rf *.json *.pyc
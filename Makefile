clean:
	rm -rf *.json *.pyc
test:
	python3 -m unittest test_unit
	rm -rf *.json *.pyc
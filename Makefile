clean:
	rm -rf *.json *.pyc
test:
	python -m unittest test_unit
	rm -rf *.json *.pyc
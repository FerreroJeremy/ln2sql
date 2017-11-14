clean:
	rm -rf *.json *.pyc
test:
	python -m unittest test_unit.SimplisticTest.test_main
	rm -rf *.json *.pyc
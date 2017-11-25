clean:
	rm -rf *.json *.pyc
test:
	pytest
	rm -rf *.json *.pyc
.PHONY: install clean

install:
	python3 -m pip install --upgrade pip setuptools wheel
	python3 -m pip install .

clean:
	rm -rf build dist *.egg-info

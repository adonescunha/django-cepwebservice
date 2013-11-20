compile_ext:
	python setup.py build_ext -i

setup:
	pip install -r test_requirements.txt

test: compile_ext
	env PYTHONPATH=$$PYTHONPATH:cepwebservice/ DJANGO_SETTINGS_MODULE=vows.sandbox.settings pyvows -vvv

ci_test:
	$(MAKE) test

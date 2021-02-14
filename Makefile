# Makefile Scripts for Installation, Unistallation and Testing limit-order-book Project
start-mongod:
	sh mongodb_init.sh

deps-install:
	echo "Installing Dependencies"
	pip install -r requirements.txt

install:
	echo "Installing Application"
	python setup.py install  --record files.txt

uninstall:
	echo "Installing Application. Please provide password on prompt."
	cat files.txt | xargs sudo rm -rf 
	# pip uninstall limit-order-book

reinstall:
	make uninstall
	make install

fresh:
	make uninstall
	make deps-install
	make install

# Run all Test Cases
run-tests:
	python -m unittest discover

run-script:
	# make install
	script_runner.py < ./sample_data/largeOrder600K.txt

run-benchmarks:
	benchmark.py

run-threaded-script:
	echo "Multithreaded script, entries are dumped to database."
	threaded_script.py < ./sample_data/largeOrder600K.txt


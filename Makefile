#
# Makefile
# Martin Užák, 2017-01-02 11:25
#

all: clean doc

.PHONY: doc test

doc: 
	$(MAKE) -C doc html

test: 
	nosetests --with-doctest

clean:
	rm -rf build 
	find . -type d -name __pycache__ | xargs rm -rfv

# vim:ft=make
#

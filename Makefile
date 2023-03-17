# Makefile for SciDataContainer

#######################################################################
# Common variable definitions
#######################################################################

ifeq ($(OS),Windows_NT)
    RMDIR := rmdir /s /q
	RM := del /q
else
    RMDIR := rm -rf
	RM := rm -f
endif

MAKE := make
PYTHON := python
GIT := git

#######################################################################
# Targets
#######################################################################

all:
	$(MAKE) -c docs all
	$(MAKE) -c python all

pypi:
	$(MAKE) -c python pypi

clean:
	-$(MAKE) -c docs clean
	-$(MAKE) -c python clean

add: clean
	$(GIT) add .

commit: add
	$(GIT) commit -am "$(MSG)"

push: commit
	$(GIT) push -u origin main

status:
	$(GIT) status

.PHONY: all pypi clean add commit push status

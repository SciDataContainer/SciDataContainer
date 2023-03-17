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
	$(MAKE) -C docs all
	$(MAKE) -C python all

pypi:
	$(MAKE) -C python pypi

clean:
	-$(MAKE) -C docs clean
	-$(MAKE) -C python clean

add: clean
	$(GIT) add .

commit: add
	-$(GIT) commit -am "$(msg)"

push: commit
	$(GIT) push -u origin main

status:
	$(GIT) status

.PHONY: all pypi clean add commit push status

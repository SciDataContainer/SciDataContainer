# Makefile for the SciDataContainer documentation

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

#######################################################################
# Sphinx configuration
#######################################################################

# You can set these variables from the command line, and the first
# also from the environment.
SPHINXOPTS    ?=
SPHINXBUILD   := sphinx-build
SOURCEDIR     := source
BUILDDIR      := build

#######################################################################
# Targets
#######################################################################

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

all: html

%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

.PHONY: help all


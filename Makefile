# Simple makefile for the SOP-FBR function

# We need to get the system's python version and define the corresponding flags
PV := $(shell python --version | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]' | cut -c 1-9)
COMPFLAGS := $(shell $(PV)-config --cflags)
LINKFLAGS := $(shell $(PV)-config --ldflags --embed)
PROGRAM=runpy

all: $(PROGRAM)

runpy: runpy.c
	gcc $(COMPFLAGS) runpy.c -o runpy $(LINKFLAGS)
clean:
	rm -f $(PROGRAM) *.o *.pyc core

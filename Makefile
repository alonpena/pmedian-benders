# Makefile — pmedian-benders (nucleo en C)
#
# Backends de solver seleccionables: make SOLVER=gurobi|scip   (default gurobi)
# Gurobi se autodetecta en /Library/gurobiXXXX/macos_universal2 si GUROBI_HOME no esta seteado.
#
# Targets:
#   make            -> binario principal ./pmedian (Etapa 5+: necesita solver)
#   make test       -> compila y corre tests del nucleo (Etapas 1-4, sin solver)
#   make clean

CC      ?= cc
CFLAGS  ?= -O2 -Wall -Wextra -std=c11
LDFLAGS ?=
LDLIBS  ?= -lm

SOLVER  ?= gurobi

# --- autodeteccion de Gurobi ---
ifeq ($(SOLVER),gurobi)
  ifeq ($(GUROBI_HOME),)
    GUROBI_HOME := $(lastword $(sort $(wildcard /Library/gurobi*/macos_universal2)))
  endif
  GRB_INC := $(GUROBI_HOME)/include
  GRB_LIB := $(GUROBI_HOME)/lib
  # nombre de la lib: libgurobiXXX.dylib -> -lgurobiXXX
  GRB_LIBNAME := $(patsubst lib%.dylib,%,$(notdir $(firstword $(wildcard $(GRB_LIB)/libgurobi[0-9]*.dylib))))
  SOLVER_CFLAGS := -I$(GRB_INC) -DUSE_GUROBI
  SOLVER_LDFLAGS := -L$(GRB_LIB)
  SOLVER_LDLIBS  := -l$(GRB_LIBNAME)
endif

CORE_SRC := src/instance.c src/sortsites.c src/separation.c

# --- tests del nucleo (no requieren solver) ---
.PHONY: test
test: build/test_core
	@DYLD_LIBRARY_PATH=$(GRB_LIB) ./build/test_core instances/toy/toy1.pmp

build/test_core: $(CORE_SRC) tests/test_core.c | build
	$(CC) $(CFLAGS) $(CORE_SRC) tests/test_core.c $(LDLIBS) -o $@

build:
	@mkdir -p build

.PHONY: clean
clean:
	rm -rf build pmedian *.o

.PHONY: info
info:
	@echo "SOLVER=$(SOLVER)"
	@echo "GUROBI_HOME=$(GUROBI_HOME)"
	@echo "GRB_LIBNAME=$(GRB_LIBNAME)"

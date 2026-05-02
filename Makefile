# Nick's Very Own Makefile
PYTHON := python3
FIGDIR := build/figures
DB     := build/research.db

.PHONY: all download simulate build-db figures clean

all: download simulate build-db figures

download:
	$(PYTHON) scripts/download.py

simulate:
	$(PYTHON) scripts/simulate_data.py

build-db:
	$(PYTHON) scripts/build_db.py

figures: $(FIGDIR)
	$(PYTHON) scripts/figures.py

$(FIGDIR):
	mkdir -p $(FIGDIR)

clean:
	rm -rf build
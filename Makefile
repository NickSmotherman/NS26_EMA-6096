# Nick's Very Own Makefile
PYTHON := python3
FIGDIR := build/figures
DB     := build/research.db

.PHONY: all download simulate build-db analyze figures clean

all: download simulate build-db analyze figures

download:
	$(PYTHON) scripts/download.py

simulate:
	$(PYTHON) scripts/simulate_data.py

build-db:
	$(PYTHON) scripts/build_db.py

analyze:
	$(PYTHON) scripts/analyze.py

figures: $(FIGDIR)
	$(PYTHON) scripts/figures.py

$(FIGDIR):
	mkdir -p $(FIGDIR)

clean:
	rm -rf build
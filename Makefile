# Nick's Very Own Makefile
TYPST  := typst compile --root .
PYTHON := python3
FIGDIR := build/figures
DB     := build/research.db

.PHONY: all download simulate build-db analyze figures grant clean

all: download simulate build-db analyze figures grant

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

grant: figures
	$(TYPST) f31/main.typ build/f31.pdf

$(FIGDIR):
	mkdir -p $(FIGDIR)

clean:
	rm -rf build
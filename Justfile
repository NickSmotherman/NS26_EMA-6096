# Justfile
compose := "podman compose"

# Default: build everything
default: all

# Build everything
all:
    {{compose}} build
    {{compose}} run --rm builder make all

# Download public data only
download:
    {{compose}} run --rm builder make download

# Generate simulated data only
simulate:
    {{compose}} run --rm builder make simulate

# Build database only
build-db:
    {{compose}} run --rm builder make build-db

# Generate figures only
figures:
    {{compose}} run --rm builder make figures

# Clean build artifacts
clean:
    rm -rf build

# Build the container image
build-image:
    {{compose}} build
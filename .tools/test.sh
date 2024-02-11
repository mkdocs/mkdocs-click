#!/bin/sh
set -e

cd "$(dirname "$0")/.."

mkdocs build -q --strict -f example/mkdocs.yml

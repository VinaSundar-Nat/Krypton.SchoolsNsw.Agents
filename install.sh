#!/bin/bash
set -e
set -o pipefail

function cleanAndRebuild(){
    cd .
    cd $1
    echo "Cleaning and rebuilding in directory: $1"
    uv cache clean
    uv sync --reinstall
    uv add -r ./requirements.txt
    uv build
}

# Clean and rebuild core-lib
cleanAndRebuild  "./core-lib"
# Clean and rebuild core-app
cleanAndRebuild "./core-app"


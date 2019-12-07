#!/usr/bin/env bash
set -e
id=$1
[[ -n "$id" ]] || (echo "puzzle id required" && exit 1)
python3 -m unittest "$id.py"

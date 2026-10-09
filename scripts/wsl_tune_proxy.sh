#!/bin/bash
# F22 proxy tuning under WSL (A3 full-pair build). Args pass through to tune_proxy.py.
set -u
cd "$(dirname "$(readlink -f "$0")")/.." || { echo "FATAL: repo path not found"; exit 1; }
[ -f experiments/src/tune_proxy.py ] || { echo "FATAL: not the repository root: $PWD"; exit 1; }
exec /root/eqc-venv/bin/python experiments/src/tune_proxy.py "$@"

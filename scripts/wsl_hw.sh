#!/bin/bash
# Metered hardware runner under WSL (Criterion H: team-lead approval required). Args pass through.
set -u
cd "$(dirname "$(readlink -f "$0")")/.." || { echo "FATAL: repo path not found"; exit 1; }
[ -f experiments/src/run_hardware.py ] || { echo "FATAL: not the repository root: $PWD"; exit 1; }
exec /root/eqc-venv/bin/python experiments/src/run_hardware.py "$@"

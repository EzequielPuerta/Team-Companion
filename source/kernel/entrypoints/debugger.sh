#!/bin/bash
set -eu

SCRIPT_PATH="$TEAM_COMPANION_PATH/setup.sh"
. "$SCRIPT_PATH"

cd "$TEAM_COMPANION_PATH"

exec python -u -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess ./client.py
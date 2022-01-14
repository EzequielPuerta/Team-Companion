#!/bin/bash
set -eu

SCRIPT_PATH="$TEAM_COMPANION_PATH/setup.sh"
. "$SCRIPT_PATH"

cd "$TEAM_COMPANION_PATH"

# exec python -m unittest discover -v -s .
exec python -m unittest discover -v -s tests
# exec python -m unittest tests.
# exec python -u -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m unittest discover tests
# exec python -u -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m unittest tests.
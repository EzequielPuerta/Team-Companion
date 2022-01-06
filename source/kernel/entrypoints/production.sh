#!/bin/bash
set -eu

SCRIPT_PATH="$TEAM_COMPANION_PATH/setup.sh"
. "$SCRIPT_PATH"

cd "$TEAM_COMPANION_PATH"

exec python -u ./client.py
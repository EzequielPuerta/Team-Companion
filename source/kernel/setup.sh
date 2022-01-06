#!/bin/bash
set -eu

USER_ID=${USER_ID:-1001}
GROUP_ID=${GROUP_ID:-1001}

# Try to create user/group, don't fail if already exist
if ! grep -q ":$GROUP_ID:$" /etc/group; then
  groupadd -g "$GROUP_ID" mercap
fi
if ! id -u "$USER_ID" &> /dev/null; then
  useradd --no-log-init --system -u "$USER_ID" -g "$GROUP_ID" mercap
  install -d -m 0755 -o "$USER_ID" -g "$GROUP_ID" /home/mercap
fi

# Change ownership of used paths to user and group Id's defined previously
chown -R "$USER_ID:$GROUP_ID" "$TEAM_COMPANION_PATH" \
    ;
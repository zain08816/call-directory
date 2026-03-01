#!/usr/bin/env bash
# Install Docker Compose plugin for Podman (user install, no sudo).
# Run from project root: ./scripts/install-compose-plugin.sh

set -e
COMPOSE_DEST="${HOME}/.docker/cli-plugins/docker-compose"
COMPOSE_URL="https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64"

mkdir -p "$(dirname "$COMPOSE_DEST")"
curl -SL "$COMPOSE_URL" -o "$COMPOSE_DEST"
chmod +x "$COMPOSE_DEST"
echo "Installed: $COMPOSE_DEST"
echo "Run: podman compose up --build"

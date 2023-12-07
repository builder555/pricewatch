#!/bin/sh
env | sed 's/^/export /' >> /etc/environment
crond
cd /app && python -m app.ui.server

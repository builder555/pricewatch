#!/bin/sh
env | sed 's/^/export /' >> /etc/environment
crond
cd /app/ui/ && python server.py

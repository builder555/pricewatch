#!/bin/sh
env | sed 's/^/export /' >> /etc/environment
crond -f

#!/bin/bash
# Export current environment variables to a file
env | grep -v "no_proxy" >> /etc/environment

# Start cron in the foreground
cron -f

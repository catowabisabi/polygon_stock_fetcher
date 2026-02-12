#!/bin/sh
# Fix ownership of mounted volumes so appuser can write
chown -R appuser:appuser /app/cache /app/logs 2>/dev/null || true

# Run the application as appuser
exec gosu appuser python run_with_polygon.py

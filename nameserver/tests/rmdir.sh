#!/usr/bin/env bash
echo "Removing directory..."
curl -X POST http://0.0.0.0:5000/rmdir/user1/kekdir/

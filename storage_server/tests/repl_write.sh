#!/bin/bash

curl -H "Content: multipart/form-data" -F 'file=@'$1 http://188.130.155.44:8031/write/$1
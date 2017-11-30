#!/bin/bash

curl -H "Content: multipart/form-data" -F 'file=@'$1 http://188.130.155.48:8020/write/$1
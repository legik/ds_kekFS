#!/bin/bash

docker run --rm -v ds_fs_storage:/usr/src/app/storage -p 8010:8010 -p 8020-8049:8020-8049 --name strorage kekisokay/ds_fs_storage_server
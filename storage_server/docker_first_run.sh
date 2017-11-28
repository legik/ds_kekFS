docker volume create ds_fs_storage
echo {} > /var/lib/docker/volumes/ds_fs_storage/_data/mapping.json
mkdir /var/lib/docker/volumes/ds_fs_storage/_data/files/
mkdir /var/lib/docker/volumes/ds_fs_storage/_data/files/tmp
touch /var/lib/docker/volumes/ds_fs_storage/_data/empty
docker run --rm -v ds_fs_storage:/usr/src/app/storage -p 8010:8010 -p 8020-8049:8020-8049 --name strorage kekisokay/ds_fs_storage_server

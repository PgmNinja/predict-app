#!/bin/sh

until [ "`docker inspect -f {{.State.Running}} backend`"=="true" ]; do
    sleep 0.1;
done;

exec "$@"
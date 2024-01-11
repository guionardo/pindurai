#!/bin/bash

# docker run --rm -it -v ./dist:/dist $(docker build -q -f pipeline/frontend.Dockerfile .)
docker build -t pindurai/frontend -f pipeline/frontend.Dockerfile .

OUT="$(pwd)/out"
mkdir -p $OUT
# rm -r "$OUT/*"

docker run --rm -it \
    -v $OUT:/out \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    pindurai/frontend
    # cp -R "/dist/*" /out

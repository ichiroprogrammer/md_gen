#!/bin/bash -e

readonly BASE_DIR=$(cd $(dirname $0); pwd)
readonly BASENAME="$(basename $0)"


cd ${BASE_DIR}/.. > /dev/null

./export/sh/find_not_utf8.sh -e ".*.png"
./tools/format.sh

./test/test.sh

cd example > /dev/null

make clean
make -j html

[[ -n "$(git diff)" ]] && echo "error !!!" && exit 1
exit 0


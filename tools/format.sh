#!/bin/bash -e

readonly BASE_DIR=$(cd $(dirname $0); pwd)
readonly BASENAME="$(basename $0)"

cd ${BASE_DIR}/.. > /dev/null

readonly PYS=$(git ls-files . | grep ".*\.py$")

black $PYS

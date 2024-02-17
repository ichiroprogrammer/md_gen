#!/bin/bash -e

declare -r BASE_DIR=$(cd $(dirname $0); pwd)

#  ./test.sh test.test_code_ref.TestCodeRef -v

cd $BASE_DIR/..

python3 -m unittest $*

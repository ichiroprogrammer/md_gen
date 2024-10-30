#!/bin/bash -e

declare -r BASE_DIR=$(cd $(dirname $0); pwd)

cd $BASE_DIR
$BASE_DIR/../export/sh/md_to_html.sh -H -x sh_data/single.md 

[[ -n "$(git diff)" ]] && echo "error !!!" && exit 1
exit 0

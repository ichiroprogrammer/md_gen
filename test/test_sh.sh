#!/bin/bash -e

declare -r BASE_DIR=$(cd $(dirname $0); pwd)

cd $BASE_DIR
$BASE_DIR/../export/sh/md_to_html.sh -H -x -o act.md sh_data/single.md 

diff sh_data/md_to_html_exp.md act.md
diff sh_data/md_to_html_exp.html act.html

rm act.md act.html



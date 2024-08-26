#!/bin/bash -e

declare -r BASE_DIR=$(cd $(dirname $0); pwd)

cd $BASE_DIR
$BASE_DIR/../export/sh/md_to_html.sh -H -x -o tako.md sh_data/single.md 

diff sh_data/md_to_html_exp.md tako.md
diff sh_data/md_to_html_exp.html tako.html

rm tako.md



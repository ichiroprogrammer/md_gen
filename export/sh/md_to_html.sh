#!/bin/bash -e

readonly BASE_DIR=$(cd $(dirname $0); pwd)
readonly BASENAME="$(basename $0)"

function help(){
    local -r exit_code=$1
    set +x

    echo "$BASENAME  [option] : "
    echo "    -o <OUT>        : generate <OUT>"
    echo "    -H              : generate NAME.html from NAME.md"
    echo "    -x              : set -x."
    echo "    -h              : show this message"


    exit $exit_code
}

while getopts "o:xhH" flag; do
    case $flag in 
    o) readonly OUT_FILE="$OPTARG" ;; 
    x)  set -x ;; 
    H) readonly OUT_HTML="true";;
    h)  help 0 ;; 
    \?) help 1 ;; 
    esac
done

shift $(expr ${OPTIND} - 1)

readonly IN_FILE=$1
readonly PY_DIR="$BASE_DIR/../py/"
readonly OUT_FILE_BASE="${IN_FILE%.*}"
readonly DB_FILE=$OUT_FILE_BASE.$$.db
readonly COMPILED="comp_$OUT_FILE_BASE.md"

$PY_DIR/md_compile.py --mds $IN_FILE -o $COMPILED $IN_FILE
$PY_DIR/md_make_db.py $DB_FILE --mds $COMPILED
$PY_DIR/md_link.py -o ${COMPILED} --db $DB_FILE $COMPILED

rm -fr $DB_FILE

if [[ -n "$OUT_HTML" ]];then 
    $PY_DIR/md_to_html.py --author "author" --title "TITLE" -o $OUT_FILE_BASE.html $COMPILED
    rm $COMPILED
fi


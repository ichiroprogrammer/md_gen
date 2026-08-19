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
    echo "    -a <AUTOR>      : add <AUTOR> to top of doc"
    echo "    -t <TITLE>      : add <TITLE> to top of doc"
    echo "    -h              : show this message"


    exit $exit_code
}

AUTOR="none"
TITLE="no tile"
while getopts "o:xhHa:t:" flag; do
    case $flag in 
    o) readonly OUT_FILE="$OPTARG" ;; 
    a) AUTOR="$OPTARG" ;; 
    t) TITLE="$OPTARG" ;; 
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
readonly COMPILED_DIR="c$$"
readonly COMPILED="$COMPILED_DIR/$IN_FILE"

trap "rm -fr $DB_FILE $COMPILED_DIR" EXIT   # 終了するときに実行

mkdir -p "$(dirname $COMPILED)"

$PY_DIR/md_compile.py --mds $IN_FILE -o $COMPILED $IN_FILE
$PY_DIR/md_make_db.py $DB_FILE --mds $COMPILED
$PY_DIR/md_link.py -o ${COMPILED} --db $DB_FILE $COMPILED


if [[ -n "$OUT_HTML" ]];then 
    $PY_DIR/md_to_html.py --author "$AUTOR" --title "$TITLE" -o $OUT_FILE_BASE.html $COMPILED
else
    if [[ -n "$OUT_FILE" ]];then 
        cp $COMPILED $OUT_FILE
    else
        cp $COMPILED $OUT_FILE_BASE.comp.md
    fi
fi


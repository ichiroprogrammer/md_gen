#!/bin/bash -e

readonly BASE_DIR=$(cd $(dirname $0); pwd)
readonly BASENAME="$(basename $0)"
readonly PY_DIR="$BASE_DIR/../py/"

function help(){
    local -r exit_code=$1
    set +x

    echo "$BASENAME  [option] <XXX.md>'s ...: "
    echo "    -o <OUT_DIR>    : generate to <OUT_DIR>/<XXX.md>. default is ./o" 
    echo "    -f              : force to exec even if <OUT_DIR> exists"
    echo "    -b <BASE_NAME>  : basenanme of output file" 
    echo "    -H              : generate XXX.html from XXX.md or <OUT_DIR>/<XXX.html>"
    echo "    -x              : set -x."
    echo "    -a <AUTOR>      : add <AUTOR> to top of doc"
    echo "    -p              : png file with plantuml code" 
    echo "    -s              : add sectin number to headlines"
    echo "    -t <TITLE>      : add <TITLE> to top of doc"
    echo "    -h              : show this message"

    exit $exit_code
}

AUTOR="none"
TITLE="no tile"
OUT_DIR="./o"
OUT_FILE_BASE=""
SEC_NUM=""
while getopts "o:psxhHa:b:t:f" flag; do
    case $flag in 
    a) AUTOR="$OPTARG" ;; 
    b) OUT_FILE_BASE="$OPTARG" ;; 
    o) readonly OUT_DIR="$OPTARG" ;; 
    s) SEC_NUM="--sec_num" ;;
    p) readonly PU_CODE="true" ;;
    t) TITLE="$OPTARG" ;; 
    f) readonly FORCE_EXEC="true";;
    x) set -x ;; 
    H) readonly OUT_HTML="true";;
    h)  help 0 ;; 
    \?) help 1 ;; 
    esac
done

shift $(expr ${OPTIND} - 1)

readonly IN_FILE_FIRST=$1
readonly IN_FILES_NUM="$#"
readonly IN_FILES="$*"
readonly COMPILE_TMP="$OUT_DIR/c"

if [[ -z "$FORCE_EXEC"  && -e "$OUT_DIR" ]] ;then 
    echo "$OUT_DIR exsits(without -f)"
    exit 1
else 
    mkdir -p $COMPILE_TMP
fi

if [[ -z "$OUT_FILE_BASE" ]];then 
    if [[ $IN_FILES_NUM == 1 ]]; then
        OUT_FILE_BASE="${IN_FILE_FIRST%.*}"
    else
        OUT_FILE_BASE="all"
    fi
fi

if [[ -n "$PU_CODE" ]];then 
    readonly OUT_FILE_BASE_PU="${OUT_FILE_BASE}_pu"
fi

readonly DB_FILE=$COMPILE_TMP/out.db

trap "rm -fr $DB_FILE $COMPILE_TMP" EXIT   # 終了するときに実行

ALL_COMPILED=""
for md in $IN_FILES
do 
    COMPILED="$COMPILE_TMP/$(basename $md)"
    echo "compiling $md to $COMPILED"
    $PY_DIR/md_compile.py --mds $IN_FILES -o $COMPILED $md
    ALL_COMPILED="$ALL_COMPILED $COMPILED"
done

$PY_DIR/md_make_db.py $DB_FILE --mds $ALL_COMPILED

ALL_LINKED=""
for compiled in $ALL_COMPILED
do 
    LINKED="$OUT_DIR/$(basename $compiled)"
    echo "linking $LINKED from $compiled"
    $PY_DIR/md_link.py $SEC_NUM -o ${LINKED} --db $DB_FILE $compiled
    ALL_LINKED="$ALL_LINKED $LINKED"
done

$PY_DIR/md_join.py -o $OUT_DIR/$OUT_FILE_BASE.md $ALL_LINKED 
if [[ -n "$PU_CODE" ]];then 
    $PY_DIR/md_inject_pu.py $OUT_DIR/$OUT_FILE_BASE.md -o $OUT_DIR/${OUT_FILE_BASE_PU}.md
fi

if [[ -n "$OUT_HTML" ]];then 
    $PY_DIR/md_to_html.py --author "$AUTOR" --title "$TITLE" -o $OUT_DIR/$OUT_FILE_BASE.html $OUT_DIR/$OUT_FILE_BASE.md
    if [[ -n "$PU_CODE" ]];then 
        $PY_DIR/md_to_html.py --author "$AUTOR" --title "$TITLE" \
            $OUT_DIR/$OUT_FILE_BASE_PU.md -o $OUT_DIR/$OUT_FILE_BASE_PU.html 
    fi
fi


#!/bin/bash -e

readonly BASE_DIR=$(cd $(dirname $0); pwd)
readonly BASENAME="$(basename $0)"

readonly PY_CMD="${BASE_DIR}/../py/plant_uml_encode.py"

function help(){
    local -r exit_code=$1
    set +x

    echo "$BASENAME  <XXX. pu> : XXX. pu to XXX.png"
    echo " <XXX.pu>           : plant uml code file"
    echo "    -h              : show this message"

    exit $exit_code
}

while getopts "xh" flag; do
    case $flag in 
    x)  set -x ;; 
    h)  help 0 ;; 
    \?) help 1 ;; 
    esac
done
shift $(expr ${OPTIND} - 1)

readonly PU_FILE=$1
PNG_FILE="${PU_FILE%.pu}.png"

$PY_CMD $PU_FILE -o $PNG_FILE


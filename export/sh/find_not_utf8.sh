#!/bin/bash -e

function help(){
    local -r exit_code=$1
    set +x

    echo "$BASENAME  [option] : find files including not UTF-8 in current directory."
    echo "    -e PTN          : export files matching PTN(grep rexp)."
    echo "    -x              : set -x."
    echo "    -h              : show this message"

    exit $exit_code
}

while getopts "e:xh" flag; do
    case $flag in 
    e)  EXCLUDE=$EXCLUDE"grep -v $OPTARG | " ;; 
    x)  set -x ;; 
    h)  help 0 ;; 
    \?) help 1 ;; 
    esac
done
EXCLUDE=$EXCLUDE"cat" 

shift $(expr ${OPTIND} - 1)

readonly FILES=$(git ls-files . | eval $EXCLUDE)

EXIT_CODE=0

for f in $FILES
do 
    encoding=$(nkf -g $f)
    if [ "$encoding" != "ASCII" -a "$encoding" != "UTF-8" ]; then
        printf "%-12s %s\n" $encoding $f
        EXIT_CODE=$LINENO
    fi
done

exit $EXIT_CODE

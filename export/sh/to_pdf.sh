#!/bin/bash -e

function help(){
    local -r exit_code=$1
    set +x

    echo "$BASENAME  [option] <NAME.html>: generate NAME.pdf from NAME.html"
    echo "    -x              : set -x."
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

readonly HTML=$1
readonly WINPATH_HTML=$(wslpath -m $HTML)
readonly WINPATH_PDF="${WINPATH_HTML%.*}".pdf

if [ ! -f $HTML ]; then
    help 1
fi

"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu \
    --no-pdf-header-footer \
    --print-to-pdf="$WINPATH_PDF" "file://$WINPATH_HTML"

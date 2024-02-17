#!/bin/bash

function help(){
    echo "$BASENAME  [option] DEPS/"
    echo "    -d    : for debug"
    echo "    -e    : file list to exclude"
    echo "    -h    : show this message"
    echo "  DEPS    : dir including *.d"

    exit $1
}

function gen_taget_files(){
    # $1 == dir including *.d

    local deps=$(find $1 -name "*.d")

    local d_files=

    for d in $deps; do
        a=$(sed -e 's/[^ ]\+: //g'  -e 's/\\//g' -e 's/[ ]\+/\n/g' $d)
        d_files="$d_files $a"
    done

    readlink -f $d_files | sort | uniq | grep -v googletest
}


while getopts ":dhe:" flag; do
    case $flag in 
    d) set -x ;; 
    e) EXCLUDE="$OPTARG" ;; 
    h) help 0 ;; 
    \?) help 1 ;; 
    esac
done

shift $(expr ${OPTIND} - 1)
set -e

[[ -z "$1" ]] && help 1

readonly TEMP="format.tmp"

# westerly
#    C++のconstのスタイルを const T -> T const に修正する
#    westerlyインストールは、
#         > sudo pip install westerly

if which westerly > /dev/null 2>&1 ; then
    readonly WESTERLY=westerly
else
    echo "skip const T -> T const because westerly not found."
    readonly WESTERLY=cat
fi

for f in $(gen_taget_files $1)
do
    if [[ -n "$EXCLUDE" ]] && [[ $f =~ $EXCLUDE ]] ; then
        clang-format $f > $TEMP
    else
	    $WESTERLY $f | clang-format > $TEMP
    fi

    diff $f $TEMP  > /dev/null 2>&1 || (mv $TEMP $f; echo "modified $(basename $f)")
done

rm -f $TEMP

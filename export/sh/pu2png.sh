#!/bin/bash

readonly BASE_DIR=$(cd $(dirname $0); pwd)
readonly BASENAME="$(basename $0)"
readonly PLANTUML="$BASE_DIR/plantuml.jar"

function install_help() {
    cat << EOS
# on ubuntu in wsl
# install env to run plantuml.jar

sudo apt update

sudo apt install openjdk-17-jdk -y      # install java
sudo apt install graphviz -y
sudo apt install plantuml -y
wget https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar -O plantuml.jar

EOS
}


function check_pkg() {

    which java > /dev/null
    if [[ $? -ne 0 ]]; then
        install_help
        exit 1
    fi

    which plantuml > /dev/null
    if [[ $? -ne 0 ]]; then
        install_help
        exit 1
    fi

    if [[ ! -e $PLANTUML  ]]; then
        install_help
        exit 1
    fi
}

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

set -e

readonly PU_FILE=$1
readonly PNG_FILE="${PU_FILE%.pu}.png"

check_pkg

java -jar $PLANTUML $PU_FILE


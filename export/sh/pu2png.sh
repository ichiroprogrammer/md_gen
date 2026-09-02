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
    echo "    -L              : generate legnd"
    echo "    -t <FMT>        : <FMT>: png(default)/svg/eps/vdx"
    echo "    -x              : set -x."
    echo "    -h              : show this message"

    exit $exit_code
}

function gen_legend() {
    readonly output="$1"
    cat << legend_EOS > $output
@startuml

legend right
  |色|意味|
  |<back:Green>　　</back>|単方向の依存|
  |<back:Orange>　　</back>|依存グラフ中の循環|
  |<back:Red>　　</back>|相互依存|
endlegend
@enduml
legend_EOS
}

FMT_opt=png
while getopts "Lxt:h" flag; do
    case $flag in 
    L) LEGEND="legend.pu" ;;
    t) FMT_opt=$OPTARG ;;
    x)  set -x ;; 
    h)  help 0 ;; 
    \?) help 1 ;; 
    esac
done
shift $(expr ${OPTIND} - 1)

readonly FMT=$FMT_opt
set -e

readonly PU_FILE=$1

check_pkg

if [[ -n "$LEGEND" ]]; then
    readonly dir=$(dirname $PU_FILE)
    readonly legend_file=${dir}/'legend.pu'
    
    gen_legend $legend_file
    java -Djava.net.useSystemProxies=true -Djava.awt.headless=true -jar $PLANTUML -t$FMT $legend_file
fi

java -Djava.net.useSystemProxies=true -Djava.awt.headless=true -jar $PLANTUML -t$FMT $PU_FILE


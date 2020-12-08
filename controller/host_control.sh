#!/bin/bash

function wait_shutdown () {
    local signal_file="${1}"

    while inotifywait_w -e close_write ${signal_file} ; do
        if [[ $(head -c 4 ${signal_file}) == "true" ]] ; then
            echo "done" > ${signal_file}
            do_shutdown
        fi
    done
}

function inotifywait_w () {
    command -v inotifywait \
        && inotifywait $* \
        || sleep 1s
}

function do_shutdown () {
    sudo shutdown -h now
    exit 0
}

ROOT="$(readlink -f $(dirname ${0})/..)"
wait_shutdown "${ROOT}/signals/controller_shutdown_signal"

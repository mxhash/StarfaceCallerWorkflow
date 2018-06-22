#!/bin/bash

dir=$(pwd -P)
query="$1"
preferred_device=""
regex=" SIP/(.+)$"

cd $dir

if [[ $query =~ $regex ]]; then
  preferred_device="SIP/${BASH_REMATCH[1]}"
fi

query=${query// SIP\/[A-Za-z0-9]*/}

exec python call.py -n "$query" -d "$preferred_device"

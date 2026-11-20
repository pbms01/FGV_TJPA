#!/bin/bash
# repete um comando até dar certo ou até o prazo (epoch em $1)
ate=$1; shift
while [ "$(date +%s)" -lt "$ate" ]; do "$@" && exit 0; sleep 60; done; exit 1

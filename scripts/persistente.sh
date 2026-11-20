#!/bin/bash
# Repete o coletor por janelas até concluir ou até o prazo (epoch UTC em $1); cada execução retoma das janelas feitas.
ate=$1; shift
while [ "$(date +%s)" -lt "$ate" ]; do
  python3 -I /home/claude/sonda/coleta_janelas.py "$@" && exit 0
  sleep 90
done
exit 1

#!/usr/bin/zsh

if [[ -n $VIRTUAL_ENV ]]; then
  exit
fi
for p in $(pew ls); do
  d=$(pew getproject $p)
  if [[ $(realpath --relative-base="$d" -- "$PWD") =~ ^/ ]]; then
    continue
  fi
  pew workon $p --no-cd > /dev/null 2>&1
  exit
done

#!/bin/bash -x

if [ "$#" -ne 1 ]; then
  echo "usage: run.sh <dat/foo.json>"
  exit -1 
fi

time ./stage1.py $1 >o1.json
time ./stage2.py o1.json >o2.json
time ./stage3.py o1.json o2.json >o3.json
time ./stage4.py o2.json o3.json >o4.md

cat o4.md

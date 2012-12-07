#!/bin/sh

(
while true
do
  python nnservice/exe/remote_learning.py $@
  sleep 600
done
) 2>&1 |  tee ~/auto_update.log

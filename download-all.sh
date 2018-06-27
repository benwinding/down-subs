#!/usr/bin/env bash

cat .temp/download-parts.txt | parallel -j 30 --colsep '\t' \
	./download-vidpart.sh {1} {2} {3}

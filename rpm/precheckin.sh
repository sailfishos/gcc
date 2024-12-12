#!/bin/bash

NAME=gcc13
SPECNAME=${NAME}.spec
ARCHES="armv7hl i486 x86_64 aarch64"
# If your %_vendor changes, please edit this too --cvm
VENDOR=meego
TOBASELIBS=""
TOBASELIBS_ARCH=""

for i in ${ARCHES} ; do
# cross spec files
    cat ./${SPECNAME} | sed -e "s#Name: .*#Name: cross-${i}-${NAME}\n%define crossarch ${i}#" > ./cross-${i}-${NAME}.spec
done

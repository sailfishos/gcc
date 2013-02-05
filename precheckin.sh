#!/bin/bash

NAME=gcc
SPECNAME=${NAME}.spec
ARCHES="armv5tel armv6l armv7l armv7hl armv7nhl armv7tnhl mipsel i486 x86_64"
# If your %_vendor changes, please edit this too --cvm
VENDOR=meego
TOBASELIBS=""
TOBASELIBS_ARCH=""

for i in ${ARCHES} ; do
# cross spec files
    cat ./${SPECNAME} | sed -e "s#Name: .*#Name: cross-${i}-${NAME}#" > ./cross-${i}-${NAME}.spec
done

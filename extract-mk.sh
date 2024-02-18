#!/usr/bin/bash

SOURCE=${1}

MAKEFILES=($(find ${SOURCE} -name Makefile))

for makefile in ${MAKEFILES[@]}; do
    dest_dir="${makefile/${SOURCE}/}"
    dest_dir="tests/${dest_dir%/*}"
    mkdir -p "${dest_dir}"
    cp "${makefile}" "${dest_dir}"
done

mks=($(find ${SOURCE} -name *.mk))

for mk in ${mks[@]}; do
    dest_dir="${mk/${SOURCE}/}"
    dest_dir="tests/${dest_dir%/*}"
    mkdir -p "${dest_dir}"
    cp "${mk}" "${dest_dir}"
done

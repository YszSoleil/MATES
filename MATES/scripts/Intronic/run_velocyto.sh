#!/bin/bash
#### $1 sample name $2 bamfile $3 barcode file $4 gtfpath
if [ -f "$1" ] && [ -f "$2" ] && [ -f "$3" ] && [ -f "$4" ]; then
    paste "$1" "$2" "$3" | while IFS="$(printf '\t')" read -r line1 line2 line3;
    do
    if [ ! -d "${line1}" ]; then
        mkdir -p "${line1}"
        else
        echo "Directory $line1 already exists."
    fi
    echo "Start Running Velocyto for ${line1}" 
    cd ${line1}
    velocyto run -b ${line3} ${line2} "$4" --dump p1
    echo "End Running Velocyto for ${line1}" 
    cd ..
fi
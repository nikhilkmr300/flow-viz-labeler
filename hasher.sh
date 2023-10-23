#! /usr/bin/env bash

function main {
    local input_dir=$1
    local output_dir=$2

    [ -d $output_dir ] || mkdir -p $output_dir

    for filepath in "$input_dir"/*; do
        local filename=$(basename -- "$filepath")
        local ext="${filename##*.}"
        local new_filename="$(shasum "$filepath" | awk '{print $1}').$ext"
        cp "$filepath" "$output_dir/$new_filename"
    done
}

main $1 $2

#!/bin/bash

function display_usage {
    echo "Usage: $0 <output_dir>"
}

if [ "$#" -ne 1 ]; then
    display_usage
    exit 1
fi

output_dir="$1"

if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

echo "Running crawler with:"
echo "Output Directory: $output_dir"
python3 py_crawl.py "$output_dir" 

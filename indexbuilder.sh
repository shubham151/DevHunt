#!/bin/bash

available_analyzers=("StandardAnalyzer" "KeywordAnalyzer" "SimpleAnalyzer" "WhitespaceAnalyzer")

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [<input_dir>] [<analyzer_option>]"
    echo "Available analyzer options: ${available_analyzers[@]}"
    #exit 1
fi

input_dir="${1:-./}"
analyzer="$2"

if [ ! -d "$input_dir" ]; then
    echo "Error: Input directory '$input_dir' does not exist."
    #exit 1
fi

if [ -z "$analyzer" ] || [[ ! " ${available_analyzers[*]} " =~ " $analyzer " ]]; then
    echo "Invalid or missing analyzer option. Using default analyzer (StandardAnalyzer)."
    analyzer="StandardAnalyzer"
fi

python3 indexing.py "$input_dir" "$analyzer"


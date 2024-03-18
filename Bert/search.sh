#!/bin/bash

function display_usage {
    echo "____________________________________________"
    echo "Usage: $0 [<input_dir>] "
    echo "___________________________________________"
}

if [ "$#" -ne 2 ]; then
    display_usage
fi
code_dir="$1"
analyzer="$2"

if [ ! -d "$code_dir" ]; then
    echo "Warning____________________________________________"
    echo "Error: Input directory '$code_dir' does not exist."
    code_dir="./"
    echo "Using Default Directory: $code_dir"
    echo "___________________________________________________"
    #exit 1
fi

if [ ! -d "$code_dir" ]; then
    mkdir -p "$code_dir"
fi

echo ""
echo "*********************** WELCOME TO DEVHUNT *************************"
python3 search.py "$code_dir" 
echo "***************************  END ***********************************"

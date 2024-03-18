if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [<input_dir>] [<output_dir>]"
    #exit 1
fi

input_dir="${1:-./}"
output_dir="${2:-./}"

if [ ! -d "$input_dir" ]; then
    echo "Error: Input directory '$input_dir' does not exist."
    #exit 1
fi

if [ ! -d "$output_dir" ]; then
    echo "Error: Output directory '$output_dir' does not exist."
    #exit 1
fi


python3 indexing.py "$input_dir" "$output_dir"


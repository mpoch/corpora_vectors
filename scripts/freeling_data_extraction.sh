#!/bin/bash

set -e

echo "" >&2
echo " --- Freeling data extraction --- " >&2
echo "" >&2

input_dir="$1"
if [ ! -d "$input_dir" ] || [ "$input_dir" == "" ] ; then
  echo "ERROR: input data dir: '$input_dir' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

output_dir="$2"
mkdir -p "$output_dir"

for f in $input_dir/*; do
    echo $f >&2
    bname=`basename "$f"`
    awk '{ if (NF>3 && $3 ~ /^[JVNA].*/ ) print $2}' "$f" \
    > "$output_dir/$bname"
done








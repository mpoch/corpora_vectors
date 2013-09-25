#!/bin/bash

set -e

help()
{
  cat <<HELP
--- Freeling data extraction ------------------------------------------------------
USAGE:   {program} <input folder> <output folder>
-----------------------------------------------------------------------------------

HELP
  exit 0
}

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
if [ ! -d "$output_dir" ] || [ "$output_dir" == "" ] ; then
  echo "ERROR: output data dir: '$output_dir' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

for f in $input_dir/*; do
    #echo $f >&2
    #echo -n "."
    bname=`basename "$f"`
    awk '{ if (NF>3 && $3 ~ /^[JVNA].*/ ) print $2}' "$f" \
    > "$output_dir/$bname"
done
echo "" >&2







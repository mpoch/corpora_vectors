#!/bin/bash

set -e

help()
{
  cat <<HELP
--- Word counts per file ----------------------------------------------------------
USAGE:   {program} <input folder> <output folder>
-----------------------------------------------------------------------------------

HELP
  exit 0
}

echo "" >&2
echo " --- word counts per file --- " >&2
echo "" >&2

input_dir="$1"
if [ ! -d "$input_dir" ] || [ "$input_dir" == "" ] ; then
  echo "ERROR: input data dir: '$input_dir' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

output_dir="$2"
if [ "$output_dir" == "" ] ; then
  echo "ERROR: output data dir: '$output_dir' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi
mkdir -p "$output_dir"

for f in "$input_dir"/*; do
  #echo $f >&2
  #echo -n "."
  bn=`basename "$f"`
  cat "$f" | \
  sort | \
  uniq -c | \
  sort -nr \
  > "$output_dir/$bn"
done
echo ""








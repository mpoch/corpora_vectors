#!/bin/bash

set -e

sed_script="scripts/weka_invalid_char_corrector.txt"

help()
{
  cat <<HELP
--- Feature selection -------------------------------------------------------------
USAGE:   {program} <input_file> <output_file>
-----------------------------------------------------------------------------------

HELP
  exit 0
}

echo "" >&2
echo " --- Feature selection --- " >&2
echo "" >&2

input_file="$1"
if [ ! -f "$input_file" ]; then
  echo "ERROR: input_file: '$input_file' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

output_file="$2"
if [ "$output_file" == "" ] ; then
  echo "ERROR: output_file: '$output_file' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

# No feature selection by now!
echo "WARNING! DUMMY FEATURE SELECTION PROCESS!" >&2
awk '{print $2}' "$input_file" | sed -f "$sed_script" | sort > "$output_file"

echo "" >&2








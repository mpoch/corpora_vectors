#!/bin/bash

set -e

fl_dir="/home/mpoch/upf_local/tools/freeling/freeling-3.0"
#fl_dir="/usr"

ca_port="40004"
es_port="50005"
en_port="60006"


help()
{
  cat <<HELP
--- Freeling Server process folder ------------------------------------------------
USAGE:   {program} <input folder> <output folder> <language>
-----------------------------------------------------------------------------------

HELP
  exit 0
}

echo "" >&2
echo " --- Freeling Server process folder --- " >&2
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

lang="$3"
if [ "$lang" == "" ] ; then
  echo "ERROR: Language: '$lang' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

if [ "$lang" == "ca" ] || [ "$lang" == "CA" ] ; then
  port=$ca_port
fi
if [ "$lang" == "es" ] || [ "$lang" == "ES" ] ; then
  port=$es_port
fi
if [ "$lang" == "EN" ] || [ "$lang" == "EN" ] ; then
  port=$en_port
fi

for f in $input_dir/*; do
    #echo $f >&2
    #echo -n "."
    bname=`basename "$f"`
    #echo $bname >&2
    cat $f | \
    python scripts/clean_utf8_data.py | \
    "$fl_dir/bin/analyzer_client" 50005 \
    > "$output_dir/$bname"
    
done








#!/bin/bash

set -e

sed_script="scripts/weka_invalid_char_corrector.txt"
classfile="tmp/01-classfile/classfile.txt"

help()
{
  cat <<HELP
--- Feature selection -------------------------------------------------------------
USAGE:   {program} <feature_selection_process> <input_folder: statistics> <output_file> <classname>
-----------------------------------------------------------------------------------

HELP
  exit 1
}

echo "" >&2
echo " --- Feature selection --- " >&2
echo "" >&2

featSel="$1"

if [ ! "$featSel" == "none" ] && [ ! "$featSel" == "xi2" ] ; then
  echo "ERROR: Feature Selection Method: '$featSel' does not exist or is not implemented!" >&2
  echo "" >&2
  help;
fi

input_dir="$2"
if [ ! -d "$input_dir" ] || [ "$input_dir" == "" ] ; then
  echo "ERROR: input data dir: '$input_dir' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

output_file="$3"
if [ "$output_file" == "" ] ; then
  echo "ERROR: output_file: '$output_file' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

classname="$4"
if [ "$classname" == "" ] ; then
  echo "WARNING: classname: '$classname' does not exist or it cannot be read!" >&2
  echo "" >&2
  #help;
fi





if [ "$featSel" == "xi2" ] ; then
	echo "Feature selection process: $featSel" >&2
	echo "classname:                 $classname" >&2
	if [ "$classname" == "" ] ; then
	  echo "ERROR: classname: '$classname' does not exist or it cannot be read!" >&2
	  echo "" >&2
	  help;
	fi

	grep "$classname" "$classfile" | awk '{print $1}' > "$classfile.in_class"
    python "scripts/xi2.py" "$input_dir/lemmas.byid" "$classfile.in_class" | sed -f "$sed_script" | sort > "$output_file"
	echo "" >&2

else
	# No feature selection by now!
	echo "WARNING! Feature selection process: None! All words will be used." >&2
	awk '{print $2}' "$input_dir/lemmas.total" | sed -f "$sed_script" | sort > "$output_file"
	echo "" >&2
fi








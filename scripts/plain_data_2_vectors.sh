#!/bin/bash

set -e

lang="$1"
if [ "$lang" == "" ] ; then
  echo "ERROR: Language: '$lang' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

# Process input files with Freeling
scripts/freeling_server_process_folder.sh tmp/01-plain-text-data tmp/02-freeling-output "$lang"

# Extract data from FL output
scripts/freeling_data_extraction.sh tmp/02-freeling-output tmp/03-freeling-extracted-data
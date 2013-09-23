#!/bin/bash

set -e

lang="$1"
if [ "$lang" == "" ] ; then
  echo "ERROR: Language: '$lang' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

# Process input files with Freeling
bash scripts/freeling_server_process_folder.sh tmp/01-plain-text-data tmp/02-freeling-output "$lang"

# Extract data from FL output
bash scripts/freeling_data_extraction.sh tmp/02-freeling-output tmp/03-freeling-extracted-data

# Count words per file
bash scripts/word_counts_per_file.sh tmp/03-freeling-extracted-data tmp/04-counts

# Corpora word statistics
python scripts/counter.py tmp/04-counts tmp/05-statistics

# Feature selection
bash scripts/feature_selection.sh tmp/05-statistics/lemmas.total tmp/06-features/features.txt


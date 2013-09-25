#!/bin/bash

set -e

lang="$1"
if [ "$lang" == "" ] ; then
  echo "ERROR: Language: '$lang' does not exist or it cannot be read!" >&2
  echo "" >&2
  help;
fi

mkdir -p tmp/01-plain-text-data
mkdir -p tmp/02-freeling-output
mkdir -p tmp/03-freeling-extracted-data
mkdir -p tmp/04-counts
mkdir -p tmp/05-statistics
mkdir -p tmp/06-features
mkdir -p tmp/07-arff

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

# Make weka vectors
python scripts/make_weka_vectors.py tmp/05-statistics/lemmas.byid tmp/06-features/features.txt -c tmp/01-classfile/classfile.txt > tmp/07-arff/vectors.arff


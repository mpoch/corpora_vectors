# Corpora vectors UPF

Software to create weka vectors from a set of texts.

# Requirements:

FREELING: http://nlp.lsi.upc.edu/freeling/

# Installation and test:

1. unizip
Simply unzip the project

2. create a temporary folder where all files will be created:

from the project root folder:
```
mkdir tmp
```

3. Copy example data from data folder into tmp folder:
```
cp -R example/* tmp/
```

Run the program with example data (example data is in Spanish):
```
bash scripts/plain_data_2_vectors.sh es
```

The resulting weka file can be found in tmp/07-arff





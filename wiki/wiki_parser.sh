#!/usr/bin/env bash

# Define a timestamp function
timestamp() {
  date +"%T"
}
echo "$(timestamp): Start.."

python3 wiki_splitter_sax.py
echo "$(timestamp): Splitting wiki page finished.."

python3 wiki_parser.py
echo "$(timestamp): Parsing each wiki page finished"

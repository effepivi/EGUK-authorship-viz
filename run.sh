#!/usr/bin/env bash

BIB_FILES=`ls data/*.bib`
CSV_OUTPUT=data/eguk_database.csv
DB_OUTPUT=data/eguk_database.db
GRAPH_JSON=eguk_authorship_network.json

rm -f $CSV_OUTPUT
src/python/bib2csv.py $BIB_FILES temp
sed 's/\\//' temp > $CSV_OUTPUT
rm -f temp

rm -f $DB_OUTPUT
src/python/csv2SQLlight.py $CSV_OUTPUT $DB_OUTPUT
# sqlite3 $DB_OUTPUT

rm -f $GRAPH_JSON articles.json conferences.json authorship.json
src/python/db2json.py $DB_OUTPUT > $GRAPH_JSON

python3 -m http.server

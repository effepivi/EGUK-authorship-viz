#!/usr/bin/env bash

BIB_FILES=`ls data/*.bib`
CSV_OUTPUT=data/eguk_database.csv
DB_OUTPUT=data/eguk_database.db
NODES_CSV=data/nodes.csv
EDGES_CSV=data/edges.csv
GRAPH_JSON=eguk_authorship_network.json

rm -f $CSV_OUTPUT
src/python/bib2csv.py $BIB_FILES temp
sed 's/\\//' temp > $CSV_OUTPUT
rm -f temp

rm -f $DB_OUTPUT
src/python/csv2SQLlight.py $CSV_OUTPUT $DB_OUTPUT
# sqlite3 $DB_OUTPUT

rm -f $NODES_CSV $EDGES_CSV
src/python/db2nodes.py $DB_OUTPUT > $NODES_CSV
src/python/db2edges.py $DB_OUTPUT > $EDGES_CSV
src/python/db2json.py $DB_OUTPUT > $GRAPH_JSON

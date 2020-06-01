#!/usr/bin/env bash

BIB_FILES=`ls data/*.bib`
CSV_OUTPUT=data/eguk_database.csv
DB_OUTPUT=data/eguk_database.db

rm -f $CSV_OUTPUT
src/python/bib2csv.py $BIB_FILES $CSV_OUTPUT

src/python/csv2SQLlight.py $CSV_OUTPUT $DB_OUTPUT
sqlite3 $DB_OUTPUT


#!/usr/bin/env python3

import sys
import bibtexparser
#import unicodecsv as csv
import csv

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode


def main():
    # There is no bibtex file to read
    if len(sys.argv) is 1:
        print("Usage: ", sys.argv[0], " bibtex_file_1.bib bibtex_file_2.bib ... bibtex_file_N.bib output.csv");
    # There is at least one bibtex file to read
    else:
        # CSV file writer
        csv_file_name = sys.argv[len(sys.argv) - 1];
        with open(csv_file_name, 'w', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', dialect='excel');

            # Create an empty list
            bib_database_set = [];

            # Process every bibtex file
            for i in range(1, len(sys.argv) - 1):

                # Open the file is read it into a string
                with open(sys.argv[i], encoding='utf-8') as bibtex_file:
                    print("Read: ", sys.argv[i]);
                    bibtex_str = bibtex_file.read();

                # Create a bibtex parser
                parser = BibTexParser()
                parser.customization = convert_to_unicode

                # Process the string and add the corresponding BibDatabase into the list
                bib_database_set.append(bibtexparser.loads(bibtex_str, parser=parser));

            # Print the number of BibDatabase objects in bib_database_set
            print(len(bib_database_set))

            # Record the max number of authors
            max_number_of_authors = 1;

            # Process all the BibDatabase of the list
            for j in range(len(bib_database_set)):

                # Find the number of authors
                for entry_key in bib_database_set[j].entries_dict:
                    # Get the authors
                    authors = bib_database_set[j].entries_dict[entry_key]['author'];

                    # Get the number of authors
                    number_of_authors = authors.count(' and ') + 1;

                    # Update the max number of authors
                    max_number_of_authors = max(number_of_authors, max_number_of_authors);

            header_row = [];
            header_row.append("\"Year\"");
            header_row.append("\"Booktitle\"");
            header_row.append("\"Title\"");
            header_row.append("\"DOI\"");
            header_row.append("\"pages\"");
            header_row.append("\"Number of authours\"");
            for i in range(1, max_number_of_authors + 1):
                header_row.append("\"author #" + str(i) + "\"");

            # Write the header in the CSV file
            csv_writer.writerow(header_row);

            # Process all the BibDatabase of the list
            for j in range(len(bib_database_set)):
                print("Process ", sys.argv[j + 1])
                # Print the bibtex entry key, author and title of the corresponding BibDatabase object
                for entry_key in bib_database_set[j].entries_dict:

                    # Create an empty row
                    row = [];

                    # This is a paper in a conference:
                    pub_venue="";
                    if bib_database_set[j].entries_dict[entry_key]['ENTRYTYPE'] == "inproceedings":
                        pub_venue = bib_database_set[j].entries_dict[entry_key]['booktitle'];
                    elif bib_database_set[j].entries_dict[entry_key]['ENTRYTYPE'] == "article":
                        pub_venue = bib_database_set[j].entries_dict[entry_key]['journal'];
                    else:
                        pub_venue = "Unknown, ask Franck what ";
                        pub_venue += bib_database_set[j].entries_dict[entry_key]['ENTRYTYPE'];
                        pub_venue += " is.";

                    # Get the year
                    year = bib_database_set[j].entries_dict[entry_key]['year'];

                    # Get the booktitle
                    booktitle = bib_database_set[j].entries_dict[entry_key]['booktitle'];

                    # Get the title
                    title = bib_database_set[j].entries_dict[entry_key]['title'];

                    # Get the authors
                    authors = bib_database_set[j].entries_dict[entry_key]['author'];

                    # Get the pages
                    if "pages" in bib_database_set[j].entries_dict[entry_key]:
                        pages = bib_database_set[j].entries_dict[entry_key]['pages'];
                    else:
                        pages = "";

                    # Get the doi
                    doi = bib_database_set[j].entries_dict[entry_key]['doi'];

                    # Get the number of authors
                    number_of_authors = authors.count(' and ') + 1;


                    row.append(year);
                    row.append("\"" + booktitle + "\"");
                    row.append("\"" + title + "\"");
                    row.append("\"" + doi + "\"");
                    row.append("\"" + pages + "\"");
                    row.append(number_of_authors);

                    # Find all the authors
                    authors_split = authors.split(' and ');
                    for author in authors_split:
                        name_components = author.split(', ');

                        if len(name_components) == 1:
                            row.append(author);
                        else:
                            firstnames = name_components[1].split(' ');
                            short_name = "";
                            for firstname in firstnames:
                                short_name += firstname[0];
                                short_name += ". ";
                            short_name += name_components[0];
                            row.append(short_name);

                    # Write the record in the CSV file
                    csv_writer.writerow(row);

                    #print("Entry key: ", entry_key)
                    '''print("Author(s): ", authors);
                    print("Booktitle: ", booktitle);
                    print("Title: ", title);
                    print("Venue: ", pub_venue);
                    print("Year: ", year);
                    print();'''


if __name__ == '__main__':
    main()

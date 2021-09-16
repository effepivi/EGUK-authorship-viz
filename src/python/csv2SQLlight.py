#!/usr/bin/env python3

import sys
import math

import pandas as pd
import sqlite3
from sqlite3 import Error

NoneType = type(None)

SQL_CREATE_CONFERENCES_TABLE = """ CREATE TABLE IF NOT EXISTS conferences (
                                    id integer PRIMARY KEY,
                                    year integer NOT NULL,
                                    full_name text NOT NULL,
                                    short_name text NOT NULL,
                                    address text
                                ); """

SQL_CREATE_AUTHORS_TABLE = """ CREATE TABLE IF NOT EXISTS authors (
                                    id integer PRIMARY KEY,
                                    fullname text NOT NULL,
                                    firstnames text NOT NULL
                                ); """

SQL_CREATE_ARTICLES_TABLE = """ CREATE TABLE IF NOT EXISTS articles (
                                    id integer PRIMARY KEY,
                                    bibtex_id text,
                                    conference_id integer NOT NULL,
                                    title text NOT NULL,
                                    doi,
                                    first_page integer,
                                    last_page integer,
                                    FOREIGN KEY (conference_id) REFERENCES conferences (id)
                                ); """

SQL_CREATE_AUTHORSHIP_TABLE = """ CREATE TABLE IF NOT EXISTS authorship (
                                    author_id integer NOT NULL ,
                                    paper_id integer NOT NULL,
                                    PRIMARY KEY(author_id,paper_id),
                                    FOREIGN KEY (author_id) REFERENCES authors (id),
                                    FOREIGN KEY (paper_id) REFERENCES articles (bibtex_id)
                                ); """


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("Cannot create the table using this request: \n", create_table_sql)
        print(e)

def create_conference(conn, conference, year, address = ""):
    """
    Create a new conference
    :param conn: Connection object
    :param conference: Conference
    :return: id of last row
    """

    temp_len = len('"Theory and Practice of Computer Graphics');


    if conference == '"EG UK Theory and Practice of Computer Graphics"':
        full_name = "Theory and Practice of Computer Graphics";
        short_name = "TPCG";
    elif conference[:temp_len] == '"Theory and Practice of Computer Graphics':
        full_name = "Theory and Practice of Computer Graphics";
        short_name = "TPCG";
    elif conference == '"Computer Graphics and Visual Computing (CGVC)"':
        full_name = "Computer Graphics and Visual Computing";
        short_name = "CGVC";
    else:
        full_name = conference;
        short_name = "unknown";

    record = (int(year), full_name, short_name, address);

    sql = ''' INSERT INTO conferences(year,full_name,short_name,address)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, record);
    return cur.lastrowid


def create_article(conn, article):
    """
        bibtex_id text ,
        conference_id integer NOT NULL,
        title text NOT NULL,
    """

    global id_of_first_author_column;

    bibtex_id = "";
    year = article['"Year"'];
    title = article['"Title"'];
    doi = article['"DOI"'];
    pages = article['"pages"'];

    if pages == '""':
        first_page = -1;
        last_page = -1;
    else:
        temp = pages.replace('"', '').split("-");
        first_page = int(temp[0]);
        last_page = int(temp[1]);

    first_page = first_page;
    last_page = last_page;

    conference_id = get_conference_id(conn, year);

    record = (bibtex_id, conference_id, title,doi,first_page,last_page);

    sql = ''' INSERT INTO articles(bibtex_id,conference_id,title,doi,first_page,last_page)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, record);

    article_id = cur.lastrowid;

    # Add all the authors
    # Look for columns of authors
    for i in range(article['"Number of authours"']):
        fullname = article[id_of_first_author_column + i];
        author_id = get_author_id(conn, fullname);
        create_authorship(conn, author_id, article_id);


def create_authorship(conn, author_id, paper_id):
    """
    author_id integer NOT NULL ,
    paper_id integer NOT NULL,
    """
    record = (author_id, paper_id);

    sql = ''' INSERT INTO authorship(author_id, paper_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, record);

def get_conference_id(conn, year):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param year: the year of the conference
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT id FROM conferences where year=" + str(year);

    cur.execute(query)

    rows = cur.fetchall()
    return rows[0][0];

def get_author_id(conn, fullname):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param fullname: the author's fullname
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT id FROM authors where fullname=\"" + fullname + "\"";

    cur.execute(query)

    rows = cur.fetchall()
    return rows[0][0];

def create_author(conn, name):
    """
    Create a new conference
    :param conn: the Connection object
    :param name: the Author's fullname
    :return: id of last row
    """

    record = (name, "");
    #print ("ADD: ", record);

    sql = ''' INSERT INTO authors(fullname, firstnames)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, record);
    return cur.lastrowid

def author_exist(conn, name):
    """
    Query all rows in the authors table
    :param conn: the Connection object
    :param name: the Author's fullname
    :return: True if the author exists in the table, false otherwise
    """
    cur = conn.cursor()
    query = "SELECT COUNT(ID) FROM authors where fullname=" + "\"" + name + "\"";

    cur.execute(query)

    rows = cur.fetchall()

    return rows[0][0];


id_of_first_author_column = 0;
def main():

    global id_of_first_author_column;

    if len(sys.argv) != 3:
        print("Usage: ", sys.argv[0], " input.csv output.db");
    else:
        csv_file_name = sys.argv[1];
        db_file_name = sys.argv[2];

        # create a database connection
        conn = create_connection(db_file_name);

        # Create the tables
        if not isinstance(conn, NoneType):

            # Create conferences table
            create_table(conn, SQL_CREATE_CONFERENCES_TABLE);

            # Create authors table
            create_table(conn, SQL_CREATE_AUTHORS_TABLE);

            # Create articles table
            create_table(conn, SQL_CREATE_ARTICLES_TABLE);

            # Create authorship table
            create_table(conn, SQL_CREATE_AUTHORSHIP_TABLE);

            # Open the CSV file
            df = pd.read_csv(csv_file_name);

            # Get all the unique combination of "Year" and "Booktitle"
            year_book_title_combination = df.groupby(['"Year"','"Booktitle"']);

            # For all combination, add a new conference
            for name,group in year_book_title_combination:

                if name[1] != '"Table of Contents and Preface"':
                    create_conference(conn, name[1], name[0]);

            id_of_first_author_column = 0;

            # Look for columns of authors
            column_index = 0;
            for column in df:
                # The column is a column of authors
                if column[:9] == '"author #':

                    if id_of_first_author_column == 0:
                        id_of_first_author_column = column_index;

                    row_is_nan = df[column].isna();

                    for author, is_nan in zip(df[column], row_is_nan):
                        if not is_nan:
                            if not author_exist(conn, author):
                                create_author(conn, author);
                column_index += 1;

            # Add every article
            for index, row in df.iterrows():
               create_article(conn, row);

           # Make sure the data is stored
            conn.commit();

        else:
            print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

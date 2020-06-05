#!/usr/bin/env python3

import sys
import math

import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error

import networkx as nx
# from networkx.algorithms import community
import community

import matplotlib.cm as cm
import matplotlib.pyplot as plt

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


def get_authors(conn):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param fullname: the author's fullname
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT id, fullname FROM authors";

    cur.execute(query)

    rows = cur.fetchall()
    return rows;


def count_publication_for_author(conn, author_id):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param fullname: the author's fullname
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT COUNT(*) FROM authorship where author_id = " + str(author_id);

    cur.execute(query)

    rows = cur.fetchall()
    return rows[0][0];


def get_articles(conn):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param year: the year of the conference
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT id, title, conference_id FROM articles";

    cur.execute(query)

    rows = cur.fetchall()
    return rows;


def get_conference(conn, id):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param year: the year of the conference
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT short_name, year FROM conferences where id=" + str(id);

    cur.execute(query)

    rows = cur.fetchall()
    return rows[0];


def get_authorship(conn, paper_id):
    """
    Query all rows in the conferences table
    :param conn: the Connection object
    :param year: the year of the conference
    :return: cnference_id
    """
    cur = conn.cursor()
    query = "SELECT author_id FROM authorship where paper_id=" + str(paper_id);

    cur.execute(query)

    rows = cur.fetchall()
    return rows;

def get_groups(conn):
    # Get the authors
    authors = get_authors(conn);

    return np.zeros(len(authors)).astype(int).flatten();

def main():

    global id_of_first_author_column;

    if len(sys.argv) is not 2:
        print("Usage: ", sys.argv[0], " input.db");
    else:
        db_file_name  = sys.argv[1];

        # create a database connection
        conn = create_connection(db_file_name);

        # Create the tables
        if conn is not None:


            # Get the authors
            authors = get_authors(conn);

            # Create the groups here
            groups = get_groups(conn);

            nodes = [];
            edges = [];

            for i, value in enumerate(zip(authors, groups)):

                author_id = value[0][0];
                author_name = value[0][1];
                nodes.append(author_id);


            d = dict();
            for paper_id, title, conference_id in get_articles(conn):
                conference = get_conference(conn, conference_id);

                co_authors = [];
                for authorship in get_authorship(conn, paper_id):
                    co_authors.append(authorship[0]);

                for author1 in co_authors:
                    for author2 in co_authors:
                        if author1 != author2:
                            key = (min(author1, author2), max(author1, author2));

                            edges.append((key[0], key[1]));

                            if not key in d:
                                d[key] = 1;
                            else:
                                d[key] += 1;




            G = nx.Graph() # Initialize a Graph object
            G.add_nodes_from(nodes) # Add nodes to the Graph
            G.add_edges_from(edges) # Add edges to the Graph
            partition = community.best_partition(G);

            groups = [];
            for k, v in partition.items():
                partition[k] = v + 1;
                groups.append((partition[k]))


            print('{\n\t"directed": false,\n\t"multigraph": false,\n\t"graph": {},\n\t"nodes": [');
            for i, value in enumerate(zip(authors, groups)):

                author_id = value[0][0];
                author_name = value[0][1];
                group  = value[1];

                nodes.append(author_name);

                if i < len(authors) - 1:
                    print('\t\t{"name": \"' + author_name + "\", \"publications\": " + str(count_publication_for_author(conn, author_id)) + ", \"group\": " + str(group) + '},');
                else:
                    print('\t\t{"name": \"' + author_name + "\", \"publications\": " + str(count_publication_for_author(conn, author_id)) + ", \"group\": " + str(group) + '}');
            print('\t],')
            print('\t"links": [')

            for i, key in enumerate(d):
                if i < len(d) - 1:
                    print('\t\t{"source": ', key[0]-1, ', "target": ', key[1]-1, ', "weight": ', d[key] / 2, '},');
                else:
                    print('\t\t{"source": ', key[0]-1, ', "target": ', key[1]-1, ', "weight": ', d[key] / 2, '}');

            print('\t]')

            print('}')






            # draw the graph
            # pos = nx.spring_layout(G)
            # # color the nodes according to their partition
            # cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
            # nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
            #                        cmap=cmap, node_color=list(partition.values()))
            # # nx.draw_networkx_edges(G, pos, alpha=0.5)
            # plt.show()

            # print(nx.info(G)) # Print information about the Graph

            df = pd.read_sql_query("SELECT * from articles", conn);
            df.to_json("articles.json", orient="records");

            df = pd.read_sql_query("SELECT * from conferences", conn)
            df.to_json("conferences.json", orient="records")

            df = pd.read_sql_query("SELECT * from authorship", conn)
            df.to_json("authorship.json", orient="records")

            # Verify that result of SQL query is stored in the dataframe
            #print(df.head())


            conn.close()
        else:
            print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

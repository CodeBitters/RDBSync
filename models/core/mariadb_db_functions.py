import logging
import re

import mariadb


def connect_to_db(db_info):
    """
    This function uses to establish the connection to the database with the given information.
    :param db_info: A dictionary that contains the database information[host, operation port, user, password, database].
    :return: Database connection object.
    """
    try:
        connection = mariadb.connect(
            host=db_info['host'],
            port=db_info['port'],
            user=db_info['user'],
            password=db_info['password'],
            database=db_info['database']
        )
        logging.info("Connected to database successfully.[" + str(connection) + "]")
        return connection
    except mariadb.Error as err:
        logging.error("Error connecting to database. [" + str(err) + "]")
        return False


def make_query(db_connection, sql_query, enable_auto_commit=False):
    """
    This function uses to execute the given query been on the given connection.
    :param db_connection: Database connection object.
    :param sql_query: SQL query willing to execute.
    :param enable_auto_commit: True if you want to enable auto commit, False otherwise.
    :return: If the query is SELECT or any which provide output, it will return the result set as a list. Otherwise,
    it will return True if the query is executed or false if it failed.
    """
    try:
        # verify auto commit
        db_connection.autocommit = enable_auto_commit
        # get cursor
        cursor = db_connection.cursor()
        # execute query
        cursor.execute(sql_query)
        if re.search('SELECT|DESCRIBE|SHOW', sql_query, re.IGNORECASE):
            logging.info("Query executed successfully. [" + sql_query + "]")
            return cursor.fetchall()
        else:
            logging.info("Query executed successfully. [" + sql_query + "]")
            return True
    except mariadb.Error as err:
        logging.error("Error executing query.[" + sql_query + "] [" + str(err) + "]")
        return False

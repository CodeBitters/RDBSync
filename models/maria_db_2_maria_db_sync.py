import logging

from models.core.mariadb_db_functions import connect_to_db, make_query


def check_user_privileges(database_connection, database_configuration):
    """
    This function uses to check the privileges of the given user.
    :param database_connection: Database connection object.
    :param database_configuration: Database configuration dictionary.
    :return: True if the user has the required privileges, False otherwise.
    """
    # build query and execute it to check the privileges
    sql_query = "SHOW GRANTS FOR " + database_configuration['user'] + "@'%';"
    query_result = make_query(db_connection=database_connection, sql_query=sql_query)

    # extract query result to identify the privileges
    # TODO currently looking for all privileges, need to change it to the required privileges
    for row in query_result:
        if 'ALL PRIVILEGES' in row[0] and database_configuration['database'] in row[0]:
            logging.info("User has all privileges on the database.")
            return True

    logging.error("User does not have all privileges on the database.")
    return False


def lock_database_from_writing(database_connection):
    """
    This function uses to lock the given database for write.
    :param database_connection: Database connection object.
    :return: True if the database is locked, False otherwise.
    """
    # list all table in the database
    sql_query = "SHOW TABLES"
    table_list = make_query(db_connection=database_connection, sql_query=sql_query, enable_auto_commit=True)
    query_result = True
    # lock table one by one
    for table in table_list:
        sql_query = "LOCK TABLES " + table[0] + " WRITE;"
        query_result = query_result and make_query(
            db_connection=database_connection,
            sql_query=sql_query,
            enable_auto_commit=True
        )

    # check the result of the query
    if query_result:
        logging.info("Database is locked for write.")
        return True
    else:
        logging.error("Database is not locked for write.")
        return False


def unlock_database_from_writing(database_connection):
    """
    This function uses to unlock the given database for write.
    :param database_connection: Database connection object.
    :return: True if the database is unlocked, False otherwise.
    """
    # build query and execute it to unlock the database
    sql_query = "UNLOCK TABLES;"
    query_result = make_query(db_connection=database_connection, sql_query=sql_query, enable_auto_commit=True)

    # check the result of the query
    if query_result:
        logging.info("Database is unlocked for write.")
        return True
    else:
        logging.error("Database is not unlocked for write.")
        return False


def identify_basic_structural_inconsistencies(source_connection, target_connection):
    """
    This function uses to identify the basic table-vice structural inconsistencies between source and target databases.
    :param source_connection: Source database connection object.
    :param target_connection: Target database connection object.
    :return: True if there is no structural inconsistencies, False otherwise.
    """
    # build query and execute it to get the table list of both database
    sql_query = "SHOW TABLES;"
    source_table_list = make_query(db_connection=source_connection, sql_query=sql_query)
    target_table_list = make_query(db_connection=target_connection, sql_query=sql_query)

    # outer appearance vice comparison
    if len(source_table_list) != len(target_table_list):
        logging.warning("Number of tables are not equal in both databases.")
        return False

    # table structure comparison
    for tables in source_table_list:
        # consider one table at a time and do the comparison
        sql_query = "DESCRIBE " + tables[0] + ";"
        source_table_structure = make_query(db_connection=source_connection, sql_query=sql_query)
        target_table_structure = make_query(db_connection=target_connection, sql_query=sql_query)

        unmatched_fields = set()
        # compare existence of each filed with target database
        # due to understand equally of the set we check subset for both sides

        # source_table -> target_table
        for field in source_table_structure:
            if field not in target_table_structure:
                unmatched_fields.add(field)

        # target_table -> source_table
        for field in target_table_structure:
            if field not in source_table_structure:
                unmatched_fields.add(field)

        if len(unmatched_fields) != 0:
            logging.warning("Field inconsistency on " + tables[0] + " table." + "[" + str(unmatched_fields) + "]")
            return False

    # if all pass return true
    return True


def operator(database_configuration):
    source_config = database_configuration['source_db']
    target_config = database_configuration['target_db']

    # establish connection
    source_connection = connect_to_db(db_info=source_config)
    target_connection = connect_to_db(db_info=target_config)

    # check the permission available for each user
    source_privilege_check = check_user_privileges(
        database_connection=source_connection,
        database_configuration=source_config
    )
    target_privilege_check = check_user_privileges(
        database_connection=target_connection,
        database_configuration=target_config
    )

    # identify permission availability for each user for respective databases
    if source_privilege_check and target_privilege_check:
        logging.info("Database privileges are OK to proceed.")
    else:
        logging.error("Database privileges are not OK to proceed.")
        exit(10)

    # lock both databases for write
    lock_source = lock_database_from_writing(database_connection=source_connection)
    lock_target = lock_database_from_writing(database_connection=target_connection)

    if lock_source and lock_target:
        logging.info("Both databases are locked for write.")
    else:
        logging.error("Both databases are not locked for write.")
        exit(20)

    # identify inconsistencies of table structure of source and target databases
    # this will eventually identify the key attribute inconsistencies
    result = identify_basic_structural_inconsistencies(
        source_connection=source_connection,
        target_connection=target_connection
    )

    if result:
        logging.info("Structural inconsistencies are not found.")
    else:
        logging.error("Structural inconsistencies are found.")

    # unlock database from write at the end
    unlock_source = unlock_database_from_writing(database_connection=source_connection)
    unlock_target = unlock_database_from_writing(database_connection=target_connection)
    if unlock_source and unlock_target:
        logging.info("Both databases are unlocked for write.")
    else:
        logging.error("Both databases are not unlocked for write.")
        exit(30)

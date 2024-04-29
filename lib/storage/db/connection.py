import os

import mysql.connector
from dotenv import load_dotenv

connection = None


def generate_select_statement(table_name, conditions, select_column):
    # Generate the SELECT statement
    select_statement = f'SELECT {select_column} FROM {table_name}'

    # Add conditions if provided
    if conditions:
        select_statement += " WHERE " + " AND ".join(conditions)

    return [select_statement]


def generate_insert_statement(args, config):
    # Generate the SELECT statement
    insert_statement = (f"INSERT INTO {config['table']} ({', '.join(args['columns'])}) VALUES "
                        f"({', '.join(['%s'] * len(args['values']))})")

    return [insert_statement, args['values']]


def get_statement(args, data, config):
    if 'select' in config:
        return generate_select_statement(args['table'], args['condition'], data['select_column'])
    elif 'insert' in config:
        return generate_insert_statement(args, config)


def connect_to_mysql():
    global connection
    try:
        if connection is None or not connection.is_connected():
            load_dotenv()
            # Establish a connection to the MySQL server
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_DATABASE'),
            )

            if connection.is_connected():
                print("Connected to MySQL database")

        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database:", error)
        return None


def get_data_from_table(args, data, config):
    global connection
    try:
        connection = connect_to_mysql()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(*get_statement(args, data, config))
        if 'select' in config:
            rows = cursor.fetchall()
            if len(rows) == 0:
                return None
            return rows[0][data['select_column']]
        else:
            connection.commit()
            return cursor.rowcount
    except mysql.connector.Error as error:
        print("Failed to execute SELECT statement:", error)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

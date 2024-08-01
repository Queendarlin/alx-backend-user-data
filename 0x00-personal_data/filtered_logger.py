#!/usr/bin/env python3
"""
Module to obfuscate data using a filtered logger
"""
import re
import os
from typing import List
import logging
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate log message by replacing field values with a redaction string

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): Log message to be obfuscated.
        separator (str): Character separating fields in the log message.

    Returns:
        str: Obfuscated log message.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern,
                  lambda m: m.group(0).split('=')[0] + '=' + redaction,
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the list of fields to obfuscate.

            Args:
                fields (List[str]): List of fields to obfuscate.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record by obfuscating specified fields.

            Args:
                record (logging.LogRecord): The log record to format.

            Returns:
                str: The formatted log record with obfuscated fields.
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


# Define PII_FIELDS with a tuple of fields considered as PII
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    Create a logger with the name 'user_data' and
    configure it with a RedactingFormatter.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Disable propagation

    # Create a StreamHandler
    handler = logging.StreamHandler()
    # Set the formatter to RedactingFormatter with PII_FIELDS
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connect to a secure MySQL database using credentials
    from environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection:
        Connection to the MySQL database.
    """
    # Get environment variables for database credentials
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME', 'holberton')

    # Connect to the MySQL database
    connection = mysql.connector.connect(username=username,
                                         password=password,
                                         host=host,
                                         db=db)
    return connection


def log_user_data():
    """
    Logs to a secure holberton database to read a users table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = f"SELECT {fields} FROM users;"
    info_logger = get_logger()
    connection = get_db()

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: f'{x[0]}={x[1]}',
                zip(columns, row),
            )
            msg = '; '.join(list(record)) + ';'
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


if __name__ == "__main__":
    log_user_data()

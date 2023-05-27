#!/usr/bin/env python3
"""
Filtered Logger module
"""

import logging
from typing import List
from mysql.connector import errorcode
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db() -> MySQLConnection:
    """
    Connect to the MySQL database and return a connection object
    """
    # Same implementation as before


def main() -> None:
    """
    Obtain a database connection using get_db and
    retrieve all rows in the users table.
    Display each row under a filtered format.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        logger.info(format_log(row))
    cursor.close()
    db.close()


def format_log(row: List[str]) -> str:
    """
    Format the log message with filtered fields
    """
    filtered_row = {
        field: '***' if field in PII_FIELDS else value
        for field, value in zip(PII_FIELDS, row)
    }
    return "; ".join(
            f"{field}={value}"
            for field, value in filtered_row.items()
    )


class RedactingFormatter(logging.Formatter):
    """
    Custom log formatter to redact sensitive information
    """

    def __init__(self, fields: List[str]):
        self.fields = fields
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        for field in self.fields:
            message = message.replace(field, "***")
        return message


if __name__ == "__main__":
    main()

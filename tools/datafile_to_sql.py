"""
Convert excel spreadsheet or csv file to SQL using pandas and SQLAlchemy.
If no connection string (in the SQLAlchemy required format) is provided, it will default to SQLite.
Allows to send custom kwargs to pandas.read_csv, pandas.read_excel methods from command line.
"""

import sys
import logging
import argparse
import pandas as pd
import sqlalchemy


def setup_logger():
    """
    Enclosing logger initialization in a function.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] - PID: %(process)d - PNAME: %(processName)s"
        " - TID: %(thread)d - TNAME: %(threadName)s"
        " - %(levelname)s - %(filename)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = setup_logger()


class SQLConnection(object):
    """
    Wrapper to simplify connection and queries to a SQLAlchemy engine connection.
    Implements the context manager protocol.
    """

    def __init__(self, **kwargs):
        """
        kwargs:
            dbname: Name of the DB that will be created
            connection_string: SQLAlchemy connection string
        """
        self.kwargs = kwargs
        self.dbname = kwargs.get("dbname", "db")
        self.connection_string = kwargs.get("connection_string", "")

    def __enter__(self):
        try:
            if not self.connection_string:
                self.sql_string = "sqlite:///{}.db".format(self.dbname)
            else:
                # Something like <mysql+mysqlconnector://root:mysql@localhost/dbname> expected
                self.sql_string = self.connection_string
            self.engine = sqlalchemy.engine.create_engine(self.sql_string)
            self.conn = self.engine.connect()
        except Exception as e:
            logger.info("Failed to connect using {}".format(self.sql_string))
            logger.debug(e)
        else:
            return self.conn

    def __exit__(self, *args, **kwargs):
        try:
            self.conn.close()
        except Exception as e:
            logger.info("Closing the established connection failed.")
            logger.debug(e)


def convert_excel_to_sqlite(filename, chunksize=500, **kwargs):
    """
    Function to convert Excel spreadsheet to SQLite DB.

    Arguments
    ---------
        filename: str with full path to source file
        kwargs:
            read_excel: dict mapping of pandas.read_excel kwargs
            dbname: name of the database to create
            to_sql_params: dict mapping of pandas.to_sql kwargs
    """
    try:
        df = pd.read_excel(filename, **kwargs.get("read_excel", {}))
        with SQLConnection(dbname=kwargs.get("dbname", filename)) as sql:
            df.to_sql(
                filename, sql, chunksize=chunksize, **kwargs.get("to_sql_params", {})
            )
    except Exception as e:
        logger.exception(e)


def convert_csv_to_sqlite(filename, chunksize=500, **kwargs):
    """
    Function to convert CSV file to SQLite DB.

    Arguments
    ---------
        filename: str with full path to source file
        kwargs:
            read_csv: dict mapping of pandas.read_csv kwargs
            dbname: name of the database to create
            to_sql_params: dict mapping of pandas.to_sql kwargs
    """
    try:
        df = pd.read_csv(filename, **kwargs.get("read_csv", {}))
        with SQLConnection(dbname=kwargs.get("dbname", filename)) as sql:
            df.to_sql(
                filename, sql, chunksize=chunksize, **kwargs.get("to_sql_params", {})
            )
    except Exception as e:
        logger.exception(e)


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", help="File to convert to SQL")
        parser.add_argument(
            "-n", "--name", help='SQL database name ("db" by default)', default="db"
        )
        parser.add_argument(
            "-c",
            "--connection",
            help="SQLAlchemy connection string (default SQLite in current directory)",
            default="sqlite:///{}.db",
        )
        parser.add_argument(
            "-k",
            "--kwargs",
            help="Uses <eval> to parse and compile the given parameter (it should define a dict)",
            default="{}",
        )
        args = parser.parse_args()

        logger.debug(vars(args))
        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)

        if args.kwargs:
            if not args.kwargs.startswith("{") or not args.kwargs.endswith("}"):
                # Expected kwargs example: -k "{'sep':'|', 'skiprows':[0]}"
                logger.info("Kwargs do not seem safe: {}".format(args.kwargs))
                sys.exit(1)

        if args.file:
            if args.file.lower().endswith("xlsx"):
                convert_excel_to_sqlite(
                    filename=args.file,
                    connection_string=args.connection,
                    dbname=args.dbname,
                    **dict(read_excel=eval(args.kwargs))
                )
            elif args.file.lower().endswith("csv"):
                convert_csv_to_sqlite(
                    filename=args.file,
                    connection_string=args.connection,
                    dbname=args.dbname,
                    **dict(read_csv=eval(args.kwargs))
                )
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()

import os
import logging
import pymysql
from dotenv import load_dotenv
from myquerybuilder import QueryBuilder


class ConnectionManager():
    def __init__(self):
        pass

    @staticmethod
    def get_db_connection():
        # get env path
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

        # load env file
        load_dotenv(dotenv_path)

        # load params
        RDS_HOST = os.environ.get("DB_HOST")
        RDS_PORT = int(os.environ.get("DB_PORT", 3306))
        NAME = os.environ.get("DB_USERNAME")
        PASSWORD = os.environ.get("DB_PASSWORD")
        DB_NAME = os.environ.get("DB_NAME")

        # we need to instantiate the logger
        logging.basicConfig()
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        try:
            cursor = pymysql.cursors.DictCursor
            connection = QueryBuilder(host=RDS_HOST,
                                      user=NAME,
                                      passwd=PASSWORD,
                                      db=DB_NAME,
                                      port=RDS_PORT,
                                      cursorclass=cursor,
                                      connect_timeout=5)
            logger.info("SUCCESS: connection to db successful")
            return connection
        except Exception as e:
            logger.exception("Database Connection Error")
            return None

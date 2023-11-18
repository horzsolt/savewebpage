import logging
import typing
import psycopg2
import os
from configparser import ConfigParser
from datetime import datetime, timezone

from download_item import DownloadItem

class PostgresHelper():

    def __init__(self) -> None:

        config_object = ConfigParser()
        config_object.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.ini"))
        serverinfo = config_object["CONFIG"]

        self.host = serverinfo["POSTGRES_HOST"]
        self.user = serverinfo["POSTGRES_USER"]
        self.pwd = serverinfo["POSTGRES_PWD"]
        self.database = serverinfo["POSTGRES_DATABASE"]
        self.schema = serverinfo["POSTGRES_SCHEMA"]
        self.conn = None

        logging.debug(f"host {self.host}")
        logging.debug(f"user {self.user}")

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, type, value, traceback) -> None:
        self._disconnect()

    def _disconnect(self) -> None:
        if (self.conn != None):
            self.conn.close()

    def _connect(self) -> None:
        logging.debug("connect to pg")
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                port=49431,
                database=self.database
            )
        except Exception as ex:
            logging.error(ex, exc_info=True)
            print(ex)

    def list_urls_to_download(self):# -> typing.List[DownloadItem]:
        '''
        [(95,
            'https://www.cybertec-postgresql.com/en/pg_resetwal-when-to-reset-the-wal-in-postgresql/',
            'postgres, wal'),
         (96,
            'https://www.cybertec-postgresql.com/en/kill-long-running-queries-in-postgresql/',
            'postgres, slowness')]
        '''

        select_command = f'SELECT id, url, tags FROM {self.schema}.urls WHERE processed = false'

        try:
            logging.debug(f"select {select_command}")
            cursor = self.conn.cursor()
            cursor.execute(select_command)

            records = cursor.fetchall()
            #logging.debug(records)
            return [DownloadItem(id, url, tags) for id, url, tags in records]
        except Exception as ex:
            logging.error(ex, exc_info=True)

    def store(self, url: str, tags: str) -> None:

        insert_command = f'''INSERT INTO {self.schema}.urls (time, url, tags, processed)
         VALUES('{datetime.now(timezone.utc)}', '{url}', '{tags}', 'false');'''

        try:
            logging.debug(f"store_record {insert_command}")
            cursor = self.conn.cursor()
            cursor.execute(insert_command)
            self.conn.commit()
        except Exception as ex:
            logging.error(ex, exc_info=True)
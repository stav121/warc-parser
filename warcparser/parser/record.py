import logging
from psycopg2.extensions import connection
from psycopg2 import DatabaseError
import validators
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class WARCRecord:
    """
    WARC record holding and unloading function.
    """

    def __init__(self, version: str, uri: str, trec_id: str, meta: [str], corpus: int) -> None:
        """
        Generate a new instance.
        :param version: The WARC version.
        :param uri: The linked URI.
        :param trec_id: The document's TREC id.
        :param meta: The metadata linked to the record.
        :param corpus: The corpus this document belongs to.
        """
        self.version = version
        self.uri = uri
        self.trec_id = trec_id
        self.meta = meta
        self.corpus = corpus

    def print(self) -> None:
        """
        Prints the record.
        """
        logging.info("Record: { version: %s, url: %s, trec_id: %s, meta: %s }",
                     self.version, self.uri, self.trec_id, len(self.meta))

    def save(self, db_con: connection) -> None:
        """
        Save the record in the given database.
        :param db_con: The Postgres connection.
        """


        cur = db_con.cursor()
        try:
            self.validate()
            cur.execute("BEGIN")
            # Prepare statement
            cur.execute(
                "INSERT INTO record_index(version, trec_id, uri, analyzed, corpus_id) VALUES (%s,%s,%s,false,%s) RETURNING id",
                (self.version, self.trec_id, self.uri, self.corpus))
            id = cur.fetchone()[0]
            if self.meta is not None:
                for meta in self.meta:
                    if meta is not None:
                        cur.execute("INSERT INTO record_meta (record, meta) VALUES (%s, %s)", (id, meta))
            cur.execute("COMMIT")
        except (Exception, DatabaseError) as error:
            logging.error("Failed to save WARC Record with id %s", self.trec_id)
            logging.error(error)
            db_con.rollback()
        finally:
            cur.close()

    def validate(self):
        """
        Validate the record's data.
        """

        if self.version is None and self.uri is None and self.trec_id is None:
            raise Exception("Cannot save WARC record to database, missing data found.")

        if not validators.url(self.uri):
            raise Exception("The provided URL is invalid.")

        version_regex = re.compile(r'WARC\/(\d+\.)?..')
        if not version_regex.match(self.version):
            raise Exception("The provided version is invalid.")

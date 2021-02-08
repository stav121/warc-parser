from psycopg2.extensions import connection
import logging
from psycopg2 import DatabaseError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class Corpus:
    """
    Corpus helper class.
    """

    def __init__(self, name: str, conn: connection) -> None:
        """
        Initialize the corpus for the current run.
        :param name: The name of the corpus.
        :param conn: The connection.
        """
        self.conn: connection = conn
        self.name: str = name
        self.id: int = None

    def setup(self) -> bool:
        """
        Setup the corpus. This function will check if the corpus exists,
        and if it does then it's ID is set, otherwise its created.
        :return: Success/Failure
        """
        cursor = self.conn.cursor()
        try:
            logging.info("Attempting to fetch corpus with name %s", self.name)
            cursor.execute("SELECT id FROM corpus_info WHERE name = %s", (self.name,))
            row = cursor.fetchone()
            if row is None:
                cursor.execute("BEGIN")
                logging.info("No corpus found, creating a new one...")
                cursor.execute("INSERT INTO corpus_info (name) VALUES (%s) RETURNING id", (self.name,))
                self.id = cursor.fetchone()
                cursor.execute("COMMIT")
            else:
                self.id = row
        except (Exception, DatabaseError) as error:
            logging.error("Failed to create the corpus, exiting")
            return False
        finally:
            cursor.close()
        return True

    def update(self) -> None:
        """
        Update the record count of the corpus.
        """

        cursor = self.conn.cursor()
        try:
            logging.info("Updating the corpus info.")
            cursor.execute("BEGIN")
            cursor.execute("""
            UPDATE corpus_info
            SET total_records = (SELECT COUNT(*) FROM record_index WHERE corpus_id = %s) 
            WHERE id = %s
            """,
                           (self.id, self.id))
            cursor.execute("COMMIT")
        except (Exception, DatabaseError) as error:
            logging.info("Failed to update the corpus info...")
        finally:
            cursor.close()

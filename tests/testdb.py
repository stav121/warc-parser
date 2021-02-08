import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class TestDB:

    def __init__(self):
        """
        Create a database connection for the tests.
        """
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="record_database",
                user="db_user",
                password="db_pass"
            )
            cur = self.conn.cursor()
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            logging.info("Connected to Postgres version: %s", db_version)
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            raise Exception(error)

    def get_cursor(self):
        """ Return a cursor to the db """
        return self.conn.cursor()

    def close(self):
        """
        Close the current db connection.
        """
        if self.conn is not None:
            self.conn.close()

    def count_record_index_rows(self) -> int:
        """
        Returns the number of rows currently in the `record_index` table.
        :return: the number of discovered rows.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM record_index")
        result = cur.fetchone()
        logging.info("Count for `record_index` table returned %s rows", result[0])
        return result[0]

    def empty_record_index_table(self):
        """
        Deletes all the rows from the `record_index` table.
        """
        logging.warning("Emptying `record_index` table...")
        cur = self.conn.cursor()
        cur.execute("BEGIN")
        cur.execute("DELETE FROM record_meta WHERE record IS NOT NULL")
        cur.execute("DELETE FROM record_index WHERE id IS NOT NULL")
        cur.execute("DELETE FROM corpus_info WHERE id IS NOT NULL")
        cur.execute("COMMIT")
        self.conn.commit()

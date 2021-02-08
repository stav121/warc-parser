from warcparser.parser.corpus import Corpus
import unittest
from tests.testdb import TestDB


class TestCorpus(unittest.TestCase):
    """
    Corpus class test.
    """

    def test_corpus(self):
        """
        Test the correct creation of a corpus.
        """
        # Stage.
        conn = TestDB()
        corpus1 = Corpus("corpus1", conn.conn)
        corpus2 = Corpus("corpus2", conn.conn)
        corpus1.setup()

        # Save the first one.
        cursor = conn.get_cursor()
        cursor.execute("SELECT COUNT(*) FROM corpus_info")
        self.assertEqual(cursor.fetchone()[0], 1)
        # Save the second one.
        corpus2.setup()
        cursor.execute("SELECT COUNT(*) FROM corpus_info")
        self.assertEqual(cursor.fetchone()[0], 2)
        # Try to save again, should not create a new one.
        corpus2.setup()
        cursor.execute("SELECT COUNT(*) FROM corpus_info")
        self.assertEqual(cursor.fetchone()[0], 2)
        cursor.close()

        # Cleanup
        conn.empty_record_index_table()
        conn.close()

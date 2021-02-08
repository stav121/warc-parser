import unittest
from warcparser.parser.context import WARCRecord
from tests.testdb import TestDB
from warcparser.parser.corpus import Corpus


class TestWARCRecord(unittest.TestCase):
    """
    Tests for warcparser.parser.context module.
    """

    @unittest.skip("Needs database to run")
    def test_warcrecord_save_with_missing_data(self):
        """
        Verify that an exception is thrown when data is missing from the record before save.
        :return:
        """
        record = WARCRecord(None, None, None, [], 0)

        record.print()

        self.assertRaises(Exception, record.save)

        with self.assertRaises(Exception) as context:
            record.save(None)

        self.assertEqual('Cannot save WARC record to database, missing data found.', str(context.exception))

    def test_warcrecord_validation_error(self):
        """
        Verify that .validate() breaks for invalid data.
        """

        record = WARCRecord('WARC/0.18', 'http://test.com', 'some-id', ["this is a meta string"], 0)
        record.validate()

        record.version = 'WAARC/0.18'
        with self.assertRaises(Exception) as context:
            record.validate()

        self.assertEqual('The provided version is invalid.', str(context.exception))

        record.uri = "htp://test."
        with self.assertRaises(Exception) as context:
            record.validate()

        self.assertEqual("The provided URL is invalid.", str(context.exception))

    def test_save_success(self):
        """
        Verify that .validate() breaks for invalid data.
        """
        connection = TestDB()
        corpus = Corpus("test_corpus", connection.conn)
        corpus.setup()
        record = WARCRecord('WARC/0.18', 'http://test.com', 'some-id', ["This is a meta string"], corpus.id)
        record.validate()

        # Verify the table is empty
        self.assertEqual(connection.count_record_index_rows(), 0)

        record.save(connection.conn)

        # One row should be created
        self.assertEqual(connection.count_record_index_rows(), 1)

        connection.empty_record_index_table()
        connection.close()


if __name__ == "__main__":
    unittest.main()

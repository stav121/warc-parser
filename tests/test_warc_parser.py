import unittest
from warcparser.parser.parser import WARCParser
from warcparser.parser.context import ParserContext
from tests.testdb import TestDB
from warcparser.parser.corpus import Corpus


class TestWARCParser(unittest.TestCase):
    """
    Tests for warcparser.parser.parser module.
    """

    def test_warc_parser_init(self):
        """
        Test the instantiation of a WARCParser instance.
        """
        con = TestDB()
        corpus = Corpus("test_corpus", con.conn)
        corpus.setup()
        context = ParserContext('test_input/test.warc.gz', con.conn, corpus.id)
        parser = WARCParser(context)

        self.assertEqual(parser.total_records, 0)
        self.assertIsNotNone(parser.context)

        con.empty_record_index_table()
        con.close()

    def test_warc_parser_gen_records(self):
        """
        Test the correct functionality of gen_records method.
        """
        con = TestDB()
        corpus = Corpus("test_corpus", con.conn)
        corpus.setup()

        context = ParserContext('test_input/test.warc.gz', con.conn, corpus.id)
        parser = WARCParser(context)

        self.assertEqual(parser.total_records, 0)
        self.assertIsNotNone(parser.context)

        parser.gen_records()

        self.assertEqual(parser.total_records, 2)
        self.assertIsNotNone(parser.context)

        con.empty_record_index_table()
        con.close()

    def test_warc_parser_parse_success(self):
        """
        Test the correct functionality of parse method.
        """
        connection = TestDB()
        corpus = Corpus("test_corpus", connection.conn)
        corpus.setup()

        context = ParserContext('test_input/test.warc.gz', connection.conn, corpus.id)
        parser = WARCParser(context)

        self.assertEqual(parser.total_records, 0)
        self.assertIsNotNone(parser.context)

        parser.parse()

        self.assertEqual(parser.total_records, 2)

        self.assertEqual(connection.count_record_index_rows(), 2)

        connection.empty_record_index_table()
        connection.close()


if __name__ == "__main__":
    unittest.main()

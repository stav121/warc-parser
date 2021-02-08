import unittest
from warcparser.parser.context import ParserContext
from warcparser.parser.corpus import Corpus

class TestParserContext(unittest.TestCase):
    """
    Tests for warcparser.parser.context module.
    """

    def test_init_fn(self):
        # Create a new Context
        context = ParserContext('test_input/test.warc.gz', None, None)
        self.assertIsNone(context.version)
        self.assertIsNone(context.uri)
        self.assertIsNone(context.trec_id)
        self.assertIs(context.file, 'test_input/test.warc.gz')
        self.assertFalse(context.contains_record())

        # Set the version, id and uri
        context.set_version("WARC/0.18")
        context.set_uri("https://test.com")
        context.set_trec_id("clueweb09_en0001_15_00000")
        context.add_meta("test meta")
        self.assertTrue(context.contains_record())

        # Unload the doc
        record = context.unload()
        self.assertIsNotNone(record)
        self.assertIs(record.version, "WARC/0.18")
        self.assertIs(record.trec_id, "clueweb09_en0001_15_00000")
        self.assertIs(len(record.meta), 1)
        self.assertIs(record.uri, "https://test.com")

        # Verify the context is empty
        self.assertIsNone(context.version)
        self.assertIsNone(context.uri)
        self.assertIsNone(context.trec_id)

    def test_unload_incomplete_record(self):
        # Create a new Context
        context = ParserContext('test_input/test.warc.gz', None, None)
        context.set_version("WARC/0.18")
        context.set_uri("https://test.com")

        # Incomplete id
        self.assertIsNone(context.trec_id)
        self.assertIs(context.file, 'test_input/test.warc.gz')
        self.assertFalse(context.contains_record())

        # Verify an exception is thrown here
        with self.assertRaises(Exception) as cxt:
            context.unload()

        self.assertEqual("Parser Context cannot be unloaded - No complete record", str(cxt.exception))


if __name__ == "__main__":
    unittest.main()

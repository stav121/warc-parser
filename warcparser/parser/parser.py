from warcparser.parser.context import ParserContext
from warcparser.parser.record import WARCRecord
import gzip
import re
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class WARCParser:
    """
    WARC Parser.
    """

    def __init__(self, context: ParserContext) -> None:
        """
        Create a new Parser instance.
        :param context: ParserContext to use.
        """
        self.context = context
        self.total_records = 0

    def gen_records(self):
        """
        Creates the WARCRecords from the input file.
        :return:
        """

        # Open the file
        warcfile = gzip.open(self.context.file, 'r')

        # Attributes to parse.
        warc_re = re.compile(r'WARC/0.18')
        warc_target_uri_re = re.compile(r'WARC-Target-URI')
        warc_trec_id_re = re.compile(r'WARC-TREC-ID')

        body = b""

        for line in warcfile:
            try:
                if warc_re.search(str(line)):
                    # Parse the tags
                    soup = BeautifulSoup(body, 'html.parser')
                    titles = soup.find('title')
                    if titles is not None:
                        for title in titles:
                            self.context.add_meta(str(title.string))
                    # New record, init
                    if self.context.contains_record():
                        self.total_records += 1
                        body = b""
                        record: WARCRecord = self.context.unload()
                        record.print()
                        record.save(self.context.connection)
                    self.context.set_version(str(line.decode('utf-8').rstrip()))
                elif warc_target_uri_re.search(str(line)):
                    self.context.set_uri(
                        str(line.decode('utf-8').rstrip()).split("WARC-Target-URI: ", 1)[1].rstrip().lower())
                elif warc_trec_id_re.search(str(line)):
                    self.context.set_trec_id(str(line.decode('utf-8').rstrip()).split("WARC-TREC-ID: ", 1)[1])
                else:
                    body += line
            except (Exception) as error:
                logging.error("An error occurred while processing..")
                logging.error(error)

        # Unload the last one
        record = self.context.unload()
        record.print()
        record.save(self.context.connection)
        self.total_records += 1

    def parse(self) -> None:
        """
        Read the given file and parse the Record's metadata.

        In the end the data is saved in the given connection.
        """

        self.gen_records()

        # Save all the records for the current file.
        logging.info("Total records found: %s", self.total_records)

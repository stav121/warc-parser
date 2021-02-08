from warcparser.parser.record import WARCRecord
from psycopg2.extensions import connection
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class ParserContext:
    """
    A ParserContext keeps the data of the currently parsed record.
    """

    def __init__(self, file: str, conn: connection, corpus: int) -> None:
        """
        Init method.
        :param file: The file to parse.
        :param conn: The DB connection to use.
        :param corpus: The corpus to link the documents to.
        """
        self.corpus: int = corpus
        self.file: str = file
        self.version: str = None
        self.uri: str = None
        self.trec_id: str = None
        self.connection = conn
        self.meta: [str] = []

    def set_version(self, version: str) -> None:
        """
        Set the current record's version attribute.
        :param version: The version string.
        """
        self.version = version

    def set_uri(self, uri: str) -> None:
        """
        Set the current record's URI.
        :param uri: The URI string.
        """
        self.uri = uri

    def set_trec_id(self, trec_id: str) -> None:
        """
        Set the TREC id of the current record.
        :param trec_id: The ID value.
        """
        self.trec_id = trec_id

    def add_meta(self, meta: str) -> None:
        """
        Add a new meta entry.
        :param meta: The meta data to add.
        """
        if meta not in self.meta and isinstance(meta, str) and meta:
            self.meta.append(meta.lower())

    def unload(self) -> WARCRecord:
        """
        Empties the current parser context and returns a new WARCRecord from the current context.
        :return: the generated WARCRecord.
        """

        if not self.contains_record():
            raise Exception("Parser Context cannot be unloaded - No complete record")

        logging.info("Unloading document: %s", self.trec_id)

        record = WARCRecord(self.version, self.uri, self.trec_id, self.meta, self.corpus)
        self.version = None
        self.uri = None
        self.trec_id = None
        self.meta = []
        return record

    def contains_record(self) -> bool:
        """
        Check if the context a full record.
        :return: True if it contains.
        """
        return self.version is not None and self.trec_id is not None and self.uri is not None

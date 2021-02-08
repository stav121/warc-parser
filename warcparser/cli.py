import logging
import psycopg2
from warcparser.helpers.filehelper import FileHelper
from warcparser.parser.parser import WARCParser
from warcparser.parser.context import ParserContext
from warcparser.parser.corpus import Corpus
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main(filename: str, config_file: str, corpus: str) -> None:
    """
    Main function, creates a parser for the given file and processes it.
    :param filename: The path to the file to read.
    :param config_file: The configuration file to use.
    :param corpus: The corpus to append to. If it doesn't exist then it gets created.
    """

    logging.info("Checking file: %s", filename)

    # Check if the file exists and is valid.
    if not FileHelper.check_war_file(filename):
        logging.error("The file '%s' doesn't exist or is invalid.", filename)
        exit(1)
    else:
        logging.info("File exists and is a WARC file.")

    # Configuration store.
    configuration = {}

    # Check if the configuration file exists.
    if not FileHelper.file_exists(config_file):
        logging.error("The configuration file '%s' does not exist.", config_file)
        exit(1)
    else:
        logging.info('Located the config file: %s', config_file)
        config_path = open(config_file, 'r')
        config = yaml.load_all(config_path, Loader=yaml.FullLoader)
        # Load the configuration.
        for conf in config:
            for n, v in conf.items():
                configuration[n] = v

    conn = None
    try:
        # connect to the PostgreSQL server
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=configuration['pg_host'],
            database=configuration['pg_database'],
            user=configuration['pg_user'],
            password=configuration['pg_password'])

        # Check the database connection.
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        logging.info('PostgresSQL database version: %s', db_version)
        cur.close()
        corpus_context = Corpus(corpus, conn)
        if corpus_context.setup():
            parser = WARCParser(ParserContext(filename, conn, corpus_context.id))
            parser.parse()
        else:
            exit(1)
        corpus_context.update()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.warning('Database connection closed.')
            exit(0)

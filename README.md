# warc-parser
![Test warc-parser](https://github.com/stav121/warc-parser/workflows/Test%20warc-parser/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/stav121/warc-parser/branch/main/graph/badge.svg?token=G6HE8HXI6I)](https://codecov.io/gh/unix121/warc-parser)
![Commit](https://img.shields.io/github/last-commit/stav121/warc-parser)
![License](https://img.shields.io/github/license/stav121/warc-parser)

WARC/0.18 File metadata parser and indexer.

### Requirements

* Python 3.6 (or greater)
* psycopg2 2.8.5
* pyyaml 5.1
* validators 0.18.2
* beautifulsoup4 4.9.3

### About

This project is developed for the purpose of extraction and indexing metadata from WARC/0.18 file format.

The input WARC/0.18 file is processed and the metadata is saved in a Postgres Database table.

### Usage

First step is to configure the database connection in the `config.yaml` environment.

Inside the database create the table specified in the `docker/init.sql` script.

Alternatively you can use the docker-compose file located in the `docker/` folder to spawn a database.

Run: `cd docker/ && docker-compose up -d`

Example usage of the script:

`python3 warcparser.py -f input/15.warc.gz -c config.yaml -n=corpus-name`

### Author

Stavros Grigoriou

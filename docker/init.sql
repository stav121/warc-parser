-----------------------
-- Table: CORPUS_INFO
-----------------------
CREATE TABLE corpus_info
(
    id            SERIAL,
    PRIMARY KEY (id),
    name          TEXT NOT NULL UNIQUE,
    total_records INT DEFAULT 0
);

COMMENT ON TABLE corpus_info IS 'The general corpus metadata.';
COMMENT ON COLUMN corpus_info.id IS 'The corpus id (auto-generated).';
COMMENT ON COLUMN corpus_info.name IS 'The corpus name (unique).';
COMMENT ON COLUMN corpus_info.total_records IS 'The corpus total record count.';

-----------------------
-- Table: CORPUS_FILES
-----------------------
CREATE TABLE corpus_files
(
    id        SERIAL,
    PRIMARY KEY (id),
    name      TEXT NOT NULL UNIQUE,
    corpus_id INT  NOT NULL REFERENCES corpus_info (id)
);

COMMENT ON TABLE corpus_files IS 'The files contained in each corpus.';
COMMENT ON COLUMN corpus_files.id IS 'The file id.';
COMMENT ON COLUMN corpus_files.name IS 'The file name (unique).';
COMMENT ON COLUMN corpus_files.corpus_id IS 'The corpus the file belongs to.';

-----------------------
-- Table: RECORD_INDEX
-----------------------
CREATE TABLE record_index
(
    id          SERIAL,
    PRIMARY KEY (id),
    trec_id     TEXT    NOT NULL,
    uri         TEXT    NOT NULL,
    version     TEXT    NOT NULL,
    analyzed    BOOLEAN NOT NULL,
    total_words INT DEFAULT 0,
    corpus_id   INT     NOT NULL REFERENCES corpus_info (id)
);

COMMENT ON TABLE record_index IS 'Record database.';
COMMENT ON COLUMN record_index.id IS 'A auto generated entry id.';
COMMENT ON COLUMN record_index.trec_id IS 'The TREC id of the document.';
COMMENT ON COLUMN record_index.uri IS 'The URL linked to the record.';
COMMENT ON COLUMN record_index.version IS 'The WARC version from the parsed document';
COMMENT ON COLUMN record_index.analyzed IS 'The record has been analyzed';
COMMENT ON COLUMN record_index.total_words IS 'The total words in the record (including meta).';
COMMENT ON COLUMN record_index.corpus_id IS 'The corpus this record belongs to.';

----------------------
-- Table: RECORD_META
----------------------
CREATE TABLE record_meta
(
    record INT  NOT NULL REFERENCES record_index (id),
    meta   TEXT NOT NULL
);

COMMENT ON TABLE record_meta IS 'The metadata linked to a record.';
COMMENT ON COLUMN record_meta.record IS 'Foreign key to the linked record';
COMMENT ON COLUMN record_meta.meta IS 'The metadata';

----------------------
-- Table: WORD_INDEX
----------------------
CREATE TABLE word_index
(
    word              TEXT             NOT NULL UNIQUE,
    PRIMARY KEY (word),
    total_appearances INT              NOT NULL DEFAULT 0,
    frequency         DOUBLE PRECISION NOT NULL DEFAULT 0.0
);

COMMENT ON TABLE word_index IS 'Index of all found words.';
COMMENT ON COLUMN word_index.word IS 'The parsed word.';
COMMENT ON COLUMN word_index.total_appearances IS 'The total appearances of the word in all documents.';
COMMENT ON COLUMN word_index.frequency IS 'The frequency of the word in all documents.';

----------------------------
-- Table: WORD_RECORD_INDEX
----------------------------
CREATE TABLE word_record_index
(
    word        TEXT             NOT NULL REFERENCES word_index (word),
    record      INT              NOT NULL REFERENCES record_index (id),
    appearances INT              NOT NULL DEFAULT 0,
    tf          DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    idf         DOUBLE PRECISION NOT NULL DEFAULT 0.0
);

COMMENT ON TABLE word_record_index IS 'The words linked to a record.';
COMMENT ON COLUMN word_record_index.word IS 'The word text.';
COMMENT ON COLUMN word_record_index.record IS 'The owner record.';
COMMENT ON COLUMN word_record_index.appearances IS 'Appearances of the word in the record.';

----------------------------
-- Table: WORD_CORPUS_INDEX
----------------------------
CREATE TABLE word_corpus_index
(
    word        TEXT             NOT NULL REFERENCES word_index (word),
    corpus      INT              NOT NULL REFERENCES corpus_info (id),
    appearances INT              NOT NULL DEFAULT 0,
    tf          DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    idf         DOUBLE PRECISION NOT NULL DEFAULT 0.0
);

COMMENT ON TABLE word_corpus_index IS 'The words linked to a corpus.';
COMMENT ON COLUMN word_corpus_index.corpus IS 'The linked corpus.';
COMMENT ON COLUMN word_corpus_index.appearances IS 'Total appearances of the word in the corpus.';
COMMENT ON COLUMN word_corpus_index.tf IS 'Term frequency in the corpus.';
COMMENT ON COLUMN word_corpus_index.idf IS 'IDF of the word in the corpus.';
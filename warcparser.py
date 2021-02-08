from warcparser.cli import main

import argparse

if __name__ == "__main__":
    """
    Main function
    """

    parser = argparse.ArgumentParser(description="WARC/18.0 file parser by Stavros Grigoriou (@unix121)")
    parser.add_argument('-f', '--file', type=str, required=True, help='input .warc file')
    parser.add_argument('-c', '--config', type=str, required=True, help='input configuration file')
    parser.add_argument('-n', '--corpus-name', type=str, required=True, help='corpus to append to')
    args = parser.parse_args()

    main(args.file, args.config, args.corpus_name)
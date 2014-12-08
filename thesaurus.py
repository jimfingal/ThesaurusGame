from unipath import Path
import logging
import requests

ROGETS_URL = "http://www.gutenberg.org/cache/epub/10681/pg10681.txt"
THESAURUS_BEGIN = 4764
THESAURUS_END = 2781002

def _retrieve_thesaurus_text():
    index_url = ROGETS_URL
    index_text = requests.get(index_url).text
    relevant_text = index_text[THESAURUS_BEGIN:THESAURUS_END]
    return relevant_text

def get_thesaurus_text():
    p = Path('./thesaurus.txt')
    
    text = None
    
    if not p.exists():
        logging.info("File doesn't exist, parsing from internet")
        text = _retrieve_thesaurus_text()
        p.write_file(text.encode('utf-8')) 
    else:
        logging.info("File exists, reading in")
        text = p.read_file().decode('utf-8')
    
    logging.info("Read text length: %s" % len(text))

    return text
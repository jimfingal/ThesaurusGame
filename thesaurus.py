from unipath import Path
import logging
import requests
import os

ROGETS_URL = "http://www.gutenberg.org/cache/epub/10681/pg10681.txt"

local_path =  os.environ.get('HOME', '.')

def _retrieve_thesaurus_text():
    index_url = ROGETS_URL
    index_text = requests.get(index_url).text
    relevant_text = index_text[4764:2781002]
    return relevant_text

def get_thesaurus_text():
    p = Path(local_path + '/thesaurus.txt')
    
    text = None
    
    if not p.exists():
        logging.info("File doesn't exist, parsing from internet")
        text = _retrieve_thesaurus_text()
        p.write_file(text.encode('utf-8'))
    else:
        logging.info("File exists, reading in")
        text = p.read_file().decode('utf-8')
    return text
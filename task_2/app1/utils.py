import logging
import pandas as pd

logger = logging.getLogger(__name__)

def make_article(file):
    try:
        return pd.read_excel(file, header=None)[0].tolist()
    except KeyError:
        logger.error("File is empty!")

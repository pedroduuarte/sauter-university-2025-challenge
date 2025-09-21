import logging 
import sys
import time

def setup_logging():
    """
    basic logging config
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("api.log", encoding="utf-8")
        ]
    )
    logger = logging.getLogger("ONS-API")
    return logger
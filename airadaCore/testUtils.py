import json
import logging
import typing

logger = logging.getLogger("airadaCore/testFunctions")

def fetch_data():
    try:
        logger.info("Throwing test/project-paper.json data")
        with open("test/project-paper.json", "r") as f:
            return json.loads(f.read())
    except:
        logger.error("Cannot parse test/project-paper.json")
import json
import logging

logger = logging.getLogger("airada.testFunctions")

def fetchData():
    try:
        logger.info("Throwing test/new-project.json data")
        with open("test/new-project.json", "r") as f:
            return json.loads(f.read())
    except:
        logger.error("Cannot parse test/new-project.json")
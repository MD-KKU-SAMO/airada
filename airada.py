AIRADA_VERSION = "1.0.0"

import logging
import datetime

from airadaCore import projectHandler, testUtils

logger = logging.getLogger("airada")
    
def errorHandler():
    logger.info("Trowing error response to server.")
    # TODO add code

def main():
    logging.basicConfig(filename="log/airada.log", level=logging.INFO)
    logger.info(f"Started @ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
    
    # Add fetching code here later
    try: 
        rawData = testUtils.fetchData()
    except:
        logger.error(f"Cannot fetch JSON file @ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        errorHandler()
    else:
        logger.info("Successfully fetch JSON string, parsing...")

        if rawData["mode"] == "project":
            logger.info("Using project mode. Invoking airada.projectHandler...")
            outputPath = projectHandler.handle(rawData)
        #     try:
        #         outputPath = projectHandler.handle(rawData)
        #     except:
        #         logger.error(f"Got error signal from airadaCore/projectHandler @ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        #         errorHandler()
        #     else:
        #         logger.info(f"Output file at {outputPath}.")
        # else:
            logger.error("UNSUPPORTED MODE DETECTED")


if __name__ == "__main__":
    main()
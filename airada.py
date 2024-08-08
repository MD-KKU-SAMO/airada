AIRADA_VERSION = "1.0.0"

import logging
from datetime import datetime

from airadaCore import projectHandler

from airadaCore.airadaTypes import jsonData, Path

from airadaDebug import testUtils

logger: logging.Logger = logging.getLogger("airada")


def error_handler():
    logger.info("Trowing error response to server.")
    # TODO add code
    ...


def main() -> None:
    logging.basicConfig(filename="log/airada.log", level=logging.INFO)
    logger.info(f"Started @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    # Add fetching code here later
    ...

    try:
        rawData: jsonData = testUtils.fetch_data()
    except:
        logger.error(f"Cannot fetch JSON file @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        error_handler()
    else:
        logger.info("Successfully fetch JSON string, parsing...")

        # COMMENT THIS IN PRODUCTION CODE
        output: Path = projectHandler.handle(rawData)

        # if rawData["mode"] == "project-paper":
        #     logger.info("Using project mode. Invoking airada.projectHandler...")
        #     try:
        #         outputPath = projectHandler.handle(rawData)
        #     except:
        #         logger.error(f"Got error signal from airadaCore/projectHandler @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        #         error_handler()
        #     else:
        #         logger.info(f"Output file at {outputPath}.")
        # else:
        #     logger.error("UNSUPPORTED MODE DETECTED")


if __name__ == "__main__":
    main()

import logging
import docx

logger = logging.getLogger("airada.projectHandler")


def handle(data: dict) -> str:
    logger.info("Parser activated.")
    docxName = "testOut.docx"
    
    # copy template to output folder
    docx.Document('./template-doc/project.docx').save(f"./output/{docxName}.docx")

    return f"./output/{docxName}"
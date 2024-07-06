import logging

import docx
import python_docx_replace

from airadaCore import utils

logger = logging.getLogger("airadaCore/projectHandler")

def getBudgetSum(budgets: list[dict]):
    return utils.moneySum([budget["price"] for budget in budgets])

def wordHandler(document: docx.Document, data: dict):
    budgetSum = getBudgetSum(data["budgets"])
    _ = {
        "projectName": str(data["projectName"]),

        "nProfessor": str(data["nTargets"]["professor"]),
        "nStaff": str(data["nTargets"]["staff"]),
        "nStudent": str(data["nTargets"]["student"]),
        "nExternal": str(data["nTargets"]["external"]),
        "nSum": str(sum(data["nTargets"].values())),

        "startDatePeriod": utils.toThaiDate(data["period"]["start"]),
        "endDatePreroid": utils.toThaiDate(data["period"]["end"]),

        "sumBudget": str(budgetSum),
        "sumBudgetText": utils.moneyToThai(budgetSum)
    }
    python_docx_replace.docx_replace(document, **_)


def paragraphHandler(document: docx.Document, data: dict):
    pass
            

def tableHandler(document: docx.Document, data: dict):
    pass

def handle(data: dict) -> str:
    logger.info("Parser activated.")
    docxName = "outDoc"
    
    # copy template to output folder
    docx.Document('./template-doc/project.docx').save(f"./output/{docxName}.docx")

    document = docx.Document(f"./output/{docxName}.docx")

    wordHandler(document, data)
    paragraphHandler(document, data)
    tableHandler(document, data)

    document.save(f"./output/{docxName}.docx")
    
    return f"./output/{docxName}.docx"
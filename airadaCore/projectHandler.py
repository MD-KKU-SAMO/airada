import logging

import docx
import python_docx_replace

from airadaCore import utils

ENUMERATED_TOPICS = [
    "rationale",
    "objective",
    "studentManager",
    "location"
]

NON_NUMERATED_TOPICS = [
    "projectName",

    "studentCouncilManager",

    "contentAdvisor",
    "technicalAdvisor",

    "nProfessor",
    "nStaff",
    "nStudent",
    "nExternal",
    "nSum",

    "periodStartDate",
    "periodEndDate",

    "budgetSum",
    "budgetSumText"
]

logger = logging.getLogger("airadaCore/projectHandler")

def sumBudget(budgets: list[dict]):
    return utils.moneySum([budget["price"] for budget in budgets])

def addSubPlaceholders(s: str, n:int) -> str:
    return "\n\t".join([f"${{{s} {i}}}" for i in range(n)])

def studentManagerText(_: dict) -> str:
    return f"{_["name"]}\t{_["id"]}\t{_["role"]}"

def studentCoucilManagerText(_:dict) -> str:
    return f"{_["name"]}\t{_["role"]}"

def replacePlaceholders(document: docx.Document, data: dict):
    # Non-numerated placeholders
    _ = {e: data[e] for e in NON_NUMERATED_TOPICS}
    python_docx_replace.docx_replace(document, **_)

    # Enumerated placeholders
    for topic in ENUMERATED_TOPICS:
        _ = {f"{topic} {i}": data[f"{topic}s"][i] for i in range(len(data[f"{topic}s"]))}
        python_docx_replace.docx_replace(document, **_)

def prepareParagraphs(document: docx.Document, data: dict):
    _ = {f"{e}s": addSubPlaceholders(e, len(data[f"{e}s"])) for e in ENUMERATED_TOPICS}
    python_docx_replace.docx_replace(document, **_)
            

def prepareTables(document: docx.Document, data: dict):
    # TODO
    pass

def handle(data: dict) -> str:
    logger.info("Parser activated.")
    docxName = "outDoc"
    
    # copy template to output folder
    docx.Document('./template-doc/project.docx').save(f"./output/{docxName}.docx")

    document = docx.Document(f"./output/{docxName}.docx")

    prepareParagraphs(document, data)
    prepareTables(document, data)

    data["budgetSum"] = sumBudget(data["budgets"])
    data["budgetSumText"] = utils.moneyToThai(data["budgetSum"])
    data["nSum"] = data["nProfessor"] + data["nStaff"] + data["nStudent"] + data["nExternal"]
    data["periodStartDate"] = utils.toThaiDate(data["periodStartDate"])
    data["periodEndDate"] = utils.toThaiDate(data["periodEndDate"])

    data["studentCouncilManager"] = studentCoucilManagerText(data["studentCouncilManager"])

    for i in range(len(data["studentManagers"])):
        data["studentManagers"][i] = studentManagerText(data["studentManagers"][i])

    replacePlaceholders(document, data)
    
    document.save(f"./output/{docxName}.docx")
    
    return f"./output/{docxName}.docx"
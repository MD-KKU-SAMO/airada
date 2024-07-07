import logging

import docx
import python_docx_replace

from airadaCore import utils

OUTPUT_PATH = "./output/outDoc.docx"
PROJECT_PAPER_TEMPLATE_PATH = './template-doc/project-paper.docx'

STEP_TABLE_INDEX = 1
BUDGET_TABLE_INDEX = 2
OKR_TABLE_INDEX = 3

ENUMERATED_TOPICS = [
    "rationale",
    "objective",
    "studentManager",
    "location",
    "budgetItem",
    "budgetPrice",
    "consequencesOKR",
    "consequencesKPI",
    "_step",
    "stepStartDate",
    "stepEndDate",
    "stepPeroid",
    "stepManager"
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

def addTableRows(document: docx.Document, n: int, index: int, swapLast:bool = False):
    for _ in range(n - 1):
        newRow = document.tables[index].add_row()
        for i in range(len(newRow.cells)):
            newRow.cells[i].text = document.tables[index].rows[1].cells[i].text.replace('#', str(_ + 1))
            newRow.cells[i].paragraphs[0].style='tableStyleProjectPaperAirada'
        
        if (swapLast):
            document.tables[index].rows[-3]._tr.addnext(newRow._tr) # swap to before last position

    for cell in document.tables[index].rows[1].cells:
        cell.text = cell.text.replace("#", "0")
        cell.paragraphs[0].style='tableStyleProjectPaperAirada'

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
    addTableRows(document, len(data["steps"]), STEP_TABLE_INDEX)
    addTableRows(document, len(data["consequences"]), OKR_TABLE_INDEX)
    addTableRows(document, len(data["budgets"]), BUDGET_TABLE_INDEX, swapLast=True)

def handle(data: dict) -> str:
    logger.info(f"Output path set to {OUTPUT_PATH}")
    logger.info(f"Template path set to {PROJECT_PAPER_TEMPLATE_PATH}")
    
    # copy template to output folder
    docx.Document(PROJECT_PAPER_TEMPLATE_PATH).save(OUTPUT_PATH)

    document = docx.Document(OUTPUT_PATH)

    data["budgetSum"] = sumBudget(data["budgets"])
    data["budgetSumText"] = utils.moneyToThai(data["budgetSum"])
    data["nSum"] = data["nProfessor"] + data["nStaff"] + data["nStudent"] + data["nExternal"]
    data["periodStartDate"] = utils.toThaiDate(data["periodStartDate"])
    data["periodEndDate"] = utils.toThaiDate(data["periodEndDate"])

    data["studentCouncilManager"] = studentCoucilManagerText(data["studentCouncilManager"])

    data["studentManagers"] = list(map(studentManagerText, data["studentManagers"]))

    data["budgetItems"] = [f"{i+1}. {data["budgets"][i]["item"]}" for i in range(len(data["budgets"]))]
    data["budgetPrices"] = [data["budgets"][i]["price"] for i in range(len(data["budgets"]))]

    data["consequencesOKRs"] = [f"{i+1}. {data["consequences"][i]["OKR"]}" for i in range(len(data["consequences"]))]
    data["consequencesKPIs"] = [data["consequences"][i]["KPI"] for i in range(len(data["consequences"]))]

    data["_steps"] = [f"{i+1}. {data["steps"][i]["step"]}" for i in range(len(data["steps"]))]
    data["stepStartDates"] = [data["steps"][i]["startDate"] for i in range(len(data["steps"]))]
    data["stepEndDates"] = [data["steps"][i]["endDate"] for i in range(len(data["steps"]))]
    data["stepPeroids"] = list(map(utils.durationFromDates, data["stepStartDates"], data["stepEndDates"]))
    data["stepManagers"] = [data["steps"][i]["manager"] for i in range(len(data["steps"]))]

    prepareParagraphs(document, data)
    prepareTables(document, data)

    replacePlaceholders(document, data)
    
    document.save(OUTPUT_PATH)
    
    return OUTPUT_PATH
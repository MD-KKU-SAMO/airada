import logging
import time 

import docx
from docx import (
    table as _Table
)
from docx.table import _Row
from docx.oxml.ns import qn

from python_docx_replace import docx_replace

from typing import Iterable, Any

from airadaCore import utils
from airadaCore.airadaTypes import Path, DateStr, MoneyStr, jsonData

OUTPUT_PATH = "./output/out.docx"
PROJECT_PAPER_TEMPLATE_PATH = './template/project-paper.docx'

STEP_TABLE_INDEX = 1
BUDGET_TABLE_INDEX = 2
OKR_TABLE_INDEX = 3
ACTIVITY_CREDIT_TABLE_INDEX = 4
SKILL_CREDIT_TABLE_INDEX = 5

ENUMERATED_TOPICS = (
    "rationale",
    "objective",
    "studentManager",
    "location",
    "budgetItem",
    "budgetPrice",
    "consequencesOKR",
    "consequencesKPI",
    "step",
    "stepStartDate",
    "stepEndDate",
    "stepPeroid",
    "stepManager"
)

NON_NUMERATED_TOPICS = (
    "projectName",

    "councilManager",

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
)

logger: logging.Logger = logging.getLogger("airadaCore/projectHandler")


def sum_budget(budgets: list[dict]) -> MoneyStr:
    return utils.sum_money([budget["price"] for budget in budgets])


def get_sub_placeholders_text(s: str, n:int) -> str:
    return "\n\t".join([f"${{{s} {i}}}" for i in range(n)])


def get_student_manager_text(_: dict) -> str:
    return f"{_["name"]}\t{_["id"]}\t{_["role"]}"


def get_coucil_manager_text(_: dict) -> str:
    return f"{_["name"]}\t{_["role"]}"


def get_numbered_list_texts_subkeys(container: Iterable[dict[str, str]], key: Any) -> list[str]:
    return [utils.get_numbered_list_text(i, text=_[key]) for i, _ in enumerate(container, 1)]


def check_checkbox(answers: list[dict[str, bool]], checkables):
    for answer, checkable in zip(answers, checkables):
        for _ in (("organizer", 0), ("participant", 1)):
            if answer[_[0]]:
                checkable.cells[_[1]].text = "☒"
                checkable.cells[_[1]].paragraphs[0].style='airadaChecklistTable'


def duplicate_last_row(n_row: int, table: _Table, swap_last: bool = False) -> None:
    for _ in range(n_row - 1):
        new_row: _Row = table.add_row()

        for cell, template_cell in zip(new_row.cells, table.rows[1].cells):
            cell.text = template_cell.text

        if (swap_last):
            table.rows[-3]._tr.addnext(new_row._tr) # swap to before last position

    # i starts at -1 to ignore header row
    for i, row in enumerate(table.rows, -1):
        for cell in row.cells:
            cell.text = cell.text.replace("#", str(i))
            cell.paragraphs[0].style='tableStyleProjectPaperAirada'


def replace_placeholders(document: docx.Document, data: dict[str, Any]) -> None:
    # Non-numerated placeholders
    _: dict[str, str] = {e: data[e] for e in NON_NUMERATED_TOPICS}
    
    # Enumerated placeholders
    for topic in ENUMERATED_TOPICS:
        _.update({f"{topic} {i}": content for i, content in enumerate(data[f"{topic}s"])})
        
    docx_replace(document, **_)


def place_paragraphs_placeholders(document: docx.Document, data: dict[str, Any]) -> None:
    _: dict[str, str] = {
        f"{e}s": get_sub_placeholders_text(e, len(data[f"{e}s"])) for e in ENUMERATED_TOPICS
    }
    docx_replace(document, **_)


def place_tables_placeholders(document: docx.Document, data: dict[str, Any]) -> None:
    duplicate_last_row(len(data["steps"]), document.tables[STEP_TABLE_INDEX])
    duplicate_last_row(len(data["consequencesOKRs"]), document.tables[OKR_TABLE_INDEX])
    duplicate_last_row(len(data["budgetItems"]), document.tables[BUDGET_TABLE_INDEX], swap_last=True)


def check_checkboxs(document: docx.Document, data: dict[str, Any]):
    activity_clickatbles = document.tables[ACTIVITY_CREDIT_TABLE_INDEX].rows[3:6] + \
                           document.tables[ACTIVITY_CREDIT_TABLE_INDEX].rows[7:11] + \
                           document.tables[ACTIVITY_CREDIT_TABLE_INDEX].rows[12:]
    check_checkbox(data["activityCredits"], activity_clickatbles)

    credit_clickatbles = document.tables[SKILL_CREDIT_TABLE_INDEX].rows[2:]
    check_checkbox(data["skillCredits"], credit_clickatbles)


def process_data(data: jsonData) -> dict[str, Any]:
    # simple copy from original date
    SIMPLE_COPY_KEYS = [
        "projectName", "rationales", "objectives", 
        "contentAdvisor", "technicalAdvisor",
        "nProfessor", "nStaff", "nStudent", "nExternal",
        "locations",
        "ratingForm",
        "activityCredits", "skillCredits"
    ]
    
    processed_data: dict[str, Any] = {k: data[k] for k in SIMPLE_COPY_KEYS}

    # data which need processing
    budget_prices: list[MoneyStr] = [_["price"] for _ in data["budgets"]]
    budget_sum: MoneyStr = utils.sum_money_str(budget_prices)

    step_start_dates: list[DateStr] = [_["startDate"] for _ in data["steps"]]
    step_end_dates: list[DateStr] = [_["endDate"] for _ in data["steps"]]

    processed_data.update({
        "nSum":             sum(data[_] for _ in ["nProfessor", "nStaff", "nStudent", "nExternal"]),
        
        "periodStartDate":  utils.toThaiDate(data["periodStartDate"]),
        "periodEndDate":    utils.toThaiDate(data["periodEndDate"]),

        "councilManager":   get_coucil_manager_text(data["studentCouncilManager"]),
        "studentManagers":  list(map(get_student_manager_text, data["studentManagers"])),

        "budgetItems":      get_numbered_list_texts_subkeys(data["budgets"], "item"),
        "budgetPrices":     budget_prices,
        "budgetSum":        budget_sum,
        "budgetSumText":    utils.get_money_thai_text(budget_sum),

        "consequencesOKRs": get_numbered_list_texts_subkeys(data["consequences"], "OKR"),
        "consequencesKPIs": [_["KPI"] for _ in data["consequences"]],

        "steps":            get_numbered_list_texts_subkeys(data["steps"], "step"),
        "stepStartDates":   step_start_dates,
        "stepEndDates":     step_end_dates,
        "stepPeroids":      list(map(utils.get_date_delta_thai_text, step_start_dates, step_end_dates)),
        "stepManagers":     [data["steps"][i]["manager"] for i in range(len(data["steps"]))]
    })

    # TODO "mostExpectedSkill", "programmes"
    return processed_data

def handle(data: jsonData) -> Path:
    logger.info(f"Output path set to {OUTPUT_PATH}")
    logger.info(f"Template path set to {PROJECT_PAPER_TEMPLATE_PATH}")
    
    # copy template to output folder
    docx.Document(PROJECT_PAPER_TEMPLATE_PATH).save(OUTPUT_PATH)

    # open copied document
    document: docx.Document = docx.Document(OUTPUT_PATH)

    # process raw JSON data
    processed_data: jsonData = process_data(data)

    place_paragraphs_placeholders(document, processed_data)
    place_tables_placeholders(document, processed_data)
    check_checkboxs(document, processed_data)
    replace_placeholders(document, processed_data)
    
    document.save(OUTPUT_PATH)
    
    return OUTPUT_PATH
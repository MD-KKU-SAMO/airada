import logging 

import docx
from docx.table import (
    Table, _Row
)

from python_docx_replace import docx_replace

from typing import Any

from airadaCore import utils

from airadaCore.airadaTypes import (
    Path, jsonData, MoneyStr
)

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
    
    "location",
    "periodStartDate",
    "periodEndDate",

    "budgetSum",
    "budgetSumText"
)

logger: logging.Logger = logging.getLogger("airadaCore/projectHandler")


def get_sub_placeholders_text(s: str, n: int) -> str:
    return "\n\t".join([f"${{{s} {i}}}" for i in range(n)])


def get_student_manager_text(_: dict) -> str:
    return f"{_["name"]}\t{_["id"]}\t{_["role"]}"


def get_coucil_manager_text(_: dict) -> str:
    return f"{_["name"]}\t{_["role"]}"


def get_clickables(table: Table) -> tuple[_Row]:
    return tuple(row for row in table.rows if row.cells[0].text == "☐")


def check_credit_table(answers: list[dict[str, bool]], checkables: list[_Row]) -> tuple[_Row]:
    for answer, checkable in zip(answers, checkables):
        for i, key in enumerate(("organizer", "participant")):
            if answer[key]:
                checkable.cells[i].text = "☒"
                checkable.cells[i].paragraphs[0].style='airadaChecklistTable'
    
    return checkables


def add_tabel_placeholders(n_row: int, table: Table, swap_last: bool = False) -> None:
    # Becasue template row was already in place, so only n-1 new rows needed.
    # rows[0] = header; rows[1] = template
    for _ in range(n_row - 1):
        new_row: _Row = table.add_row()

        for cell, template_cell in zip(new_row.cells, table.rows[1].cells):
            cell.text = template_cell.text

        # Swap to before last position. Primary used in budget table
        if (swap_last): 
            table.rows[-3]._tr.addnext(new_row._tr)

    # if swap_last == True → skip formatting last row
    rows = table.rows[1:-1] if swap_last else table.rows[1:]
    
    # [1:] to skip header row
    for i, row in enumerate(rows) :
        for cell in row.cells:
            cell.text = cell.text.replace("#", str(i))
            cell.paragraphs[0].style ='tableStyleProjectPaperAirada'


def replace_placeholders(document: docx.Document, data: dict[str, Any]) -> None:
    # Non-numerated placeholders is simply replaced
    _: dict[str, str] = {e: data[e] for e in NON_NUMERATED_TOPICS}
    
    # Enumerated placeholders. Placeholder index starts at 0.
    for topic in ENUMERATED_TOPICS:
        _.update({f"{topic} {i}": content for i, content in enumerate(data[f"{topic}s"])})

    docx_replace(document, **_)


def prepare_paragraphs(document: docx.Document, data: dict[str, Any]) -> None:
    _: dict[str, str] = {
        f"{e}s": get_sub_placeholders_text(e, len(data[f"{e}s"])) for e in ENUMERATED_TOPICS
    }

    docx_replace(document, **_)


def prepare_tables(tables: list[Table], data: dict[str, Any]) -> None:
    add_tabel_placeholders(len(data["steps"]), tables[STEP_TABLE_INDEX])
    add_tabel_placeholders(len(data["consequencesOKRs"]), tables[OKR_TABLE_INDEX])
    add_tabel_placeholders(len(data["budgetItems"]), tables[BUDGET_TABLE_INDEX], swap_last=True)


def handle_credit_section(document: docx.Document, data: dict[str, Any]) -> None:
    # Filter only row with templated blank checkbox ☐
    activity_checkables: tuple[_Row] = get_clickables(document.tables[ACTIVITY_CREDIT_TABLE_INDEX])
    check_credit_table(data["activityCredits"], activity_checkables)
    
    skill_checkables: tuple[_Row] = get_clickables(document.tables[SKILL_CREDIT_TABLE_INDEX])
    check_credit_table(data["skillCredits"], skill_checkables)
    
    most_expected_text = skill_checkables[data["mostExpectedSkill"]].cells[2].text.replace("\xa0\n", "")
    docx_replace(document, mostExpectedSkill=most_expected_text)


def process_data(data: jsonData) -> dict[str, Any]:
    # simple copy from original date
    SIMPLE_COPY_KEYS: tuple[str] = (
        "projectName", "rationales", "objectives", 
        "contentAdvisor", "technicalAdvisor",
        "nProfessor", "nStaff", "nStudent", "nExternal",
        "location",
        "ratingForm",
    )
    processed_data: dict[str, str|tuple] = {k: data[k] for k in SIMPLE_COPY_KEYS}

    processed_data.update({
        "nSum":             str(sum(data[_] for _ in ("nProfessor", "nStaff", "nStudent", "nExternal"))),
        
        "periodStartDate":  utils.toThaiDate(data["periodStartDate"]),
        "periodEndDate":    utils.toThaiDate(data["periodEndDate"]),

        "councilManager":   get_coucil_manager_text(data["studentCouncilManager"]),
        "studentManagers":  tuple(map(get_student_manager_text, data["studentManagers"])),

        "budgetItems":      utils.each_to_numbered_list("item", data["budgets"]),

        "budgetPrices":     (budget_prices := utils.get_each("price", data["budgets"])),
        "budgetSum":        (budget_sum := utils.sum_money_str(budget_prices)),
        "budgetSumText":    utils.get_money_thai_text(budget_sum),

        "consequencesOKRs": utils.each_to_numbered_list("OKR", data["consequences"]),
        "consequencesKPIs": utils.get_each("KPI", data["consequences"]),

        "steps":            utils.each_to_numbered_list("step", data["steps"]),
        "stepStartDates":   (step_start_dates := utils.get_each("startDate", data["steps"])),
        "stepEndDates":     (step_end_dates := utils.get_each("endDate", data["steps"])),
        "stepPeroids":      tuple(map(utils.get_date_delta_thai_text, step_start_dates, step_end_dates)),
        "stepManagers":     utils.get_each("manager", data["steps"])
    })

    # TODO "programmes"
    return processed_data


def handle(data: jsonData) -> Path:
    logger.info(f"Output path set to {OUTPUT_PATH}")
    logger.info(f"Template path set to {PROJECT_PAPER_TEMPLATE_PATH}")
    
    # copy template to output folder
    docx.Document(PROJECT_PAPER_TEMPLATE_PATH).save(OUTPUT_PATH)

    # open copied document
    document: docx.Document = docx.Document(OUTPUT_PATH)
    
    # credit section are handled separately for simplicity
    handle_credit_section(document, data)

    # process raw JSON data
    processed_data: jsonData = process_data(data) 

    prepare_paragraphs(document, processed_data)
    prepare_tables(document.tables, processed_data)
    
    replace_placeholders(document, processed_data)
    
    document.save(OUTPUT_PATH)
    
    return OUTPUT_PATH
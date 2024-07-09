import logging

import docx
import docx.table
import python_docx_replace

from airadaCore import utils, airadaTypes

OUTPUT_PATH = "./output/out.docx"
PROJECT_PAPER_TEMPLATE_PATH = './template/project-paper.docx'

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
    "step",
    "stepStartDate",
    "stepEndDate",
    "stepPeroid",
    "stepManager"
]

NON_NUMERATED_TOPICS = [
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
]

logger: logging.Logger = logging.getLogger("airadaCore/projectHandler")

def sum_budget(budgets: list[dict]) -> str:
    return utils.sum_money([budget["price"] for budget in budgets])

def get_sub_placeholders_text(s: str, n:int) -> str:
    return "\n\t".join([f"${{{s} {i}}}" for i in range(n)])

def get_student_manager_text(_: dict) -> str:
    return f"{_["name"]}\t{_["id"]}\t{_["role"]}"

def get_coucil_manager_text(_:dict) -> str:
    return f"{_["name"]}\t{_["role"]}"

def add_rows_to_table(document: docx.Document, n: int, index: int, swap_last: bool = False) -> None:
    for _ in range(n - 1):
        new_row: docx.table._Row = document.tables[index].add_row()
        for i in range(len(new_row.cells)):
            new_row.cells[i].text = document.tables[index].rows[1].cells[i].text.replace('#', str(_ + 1))
            new_row.cells[i].paragraphs[0].style='tableStyleProjectPaperAirada'
        
        if (swap_last):
            document.tables[index].rows[-3]._tr.addnext(new_row._tr) # swap to before last position

    for cell in document.tables[index].rows[1].cells:
        cell.text = cell.text.replace("#", "0")
        cell.paragraphs[0].style='tableStyleProjectPaperAirada'

def replace_placeholders(document: docx.Document, data: airadaTypes.JSON_data) -> None:
    # Non-numerated placeholders
    _: dict[str, str] = {e: data[e] for e in NON_NUMERATED_TOPICS}
    
    # Enumerated placeholders
    for topic in ENUMERATED_TOPICS:
        _.update({f"{topic} {i}": data[f"{topic}s"][i] for i in range(len(data[f"{topic}s"]))})
    python_docx_replace.docx_replace(document, **_)

def place_paragraphs_placeholders(document: docx.Document, data: airadaTypes.JSON_data) -> None:
    _: dict[str, str] = {
        f"{e}s": get_sub_placeholders_text(e, len(data[f"{e}s"])) for e in ENUMERATED_TOPICS
    }
    python_docx_replace.docx_replace(document, **_)

def place_tables_placeholders(document: docx.Document, data: airadaTypes.JSON_data) -> None:
    add_rows_to_table(document, len(data["steps"]), STEP_TABLE_INDEX)
    add_rows_to_table(document, len(data["consequencesOKRs"]), OKR_TABLE_INDEX)
    add_rows_to_table(document, len(data["budgetItems"]), BUDGET_TABLE_INDEX, swap_last=True)

def process_data(data: airadaTypes.JSON_data) -> airadaTypes.JSON_data:
    # simple copy from original date
    SIMPLE_COPY_KEYS = [
        "projectName", "rationales", "objectives", 
        "contentAdvisor", "technicalAdvisor",
        "nProfessor", "nStaff", "nStudent", "nExternal",
        "locations",
        "ratingForm"
    ]
    processed_data: airadaTypes.JSON_data = {k: data[k] for k in SIMPLE_COPY_KEYS}

    # data which need processing
    budgets_size: int = len(data["budgets"])
    budget_prices: list[airadaTypes.money_str] = [data["budgets"][_]["price"] for _ in range(budgets_size)]
    budget_sum: airadaTypes.money_str = utils.sum_money_str(budget_prices)

    consequences_size: int = len(data["consequences"])

    step_size: int = len(data["steps"])
    step_start_dates: list[airadaTypes.date_str] = [data["steps"][i]["startDate"] for i in range(step_size)]
    step_end_dates: list[airadaTypes.date_str] = [data["steps"][i]["endDate"] for i in range(step_size)]

    processed_data.update({
        "nSum":             sum(data[_] for _ in ["nProfessor", "nStaff", "nStudent", "nExternal"]),
        
        "periodStartDate":  utils.toThaiDate(data["periodStartDate"]),
        "periodEndDate":    utils.toThaiDate(data["periodEndDate"]),

        "councilManager":   get_coucil_manager_text(data["studentCouncilManager"]),
        "studentManagers":  list(map(get_student_manager_text, data["studentManagers"])),

        "budgetItems":      [utils.get_numbered_list_text(i+1, text=data["budgets"][i]["item"]) for i in range(budgets_size)],
        "budgetPrices":     budget_prices,
        "budgetSum":        budget_sum,
        "budgetSumText":    utils.get_money_thai_text(budget_sum),

        "consequencesOKRs": [utils.get_numbered_list_text(i+1, text=data["consequences"][i]["OKR"]) for i in range(consequences_size)],
        "consequencesKPIs": [data["consequences"][i]["KPI"] for i in range(len(data["consequences"]))],

        "steps":            [utils.get_numbered_list_text(i+1, text=data["steps"][i]["step"]) for i in range(step_size)],
        "stepStartDates":   step_start_dates,
        "stepEndDates":     step_end_dates,
        "stepPeroids":      list(map(utils.get_date_delta_thai_text, step_start_dates, step_end_dates)),
        "stepManagers":     [data["steps"][i]["manager"] for i in range(len(data["steps"]))]
    })

    # TODO "mostExpectedSkill",  "activityCredits", "skillCredits", "programmes"
    return processed_data

def handle(data: airadaTypes.JSON_data) -> airadaTypes.path:
    logger.info(f"Output path set to {OUTPUT_PATH}")
    logger.info(f"Template path set to {PROJECT_PAPER_TEMPLATE_PATH}")
    
    # copy template to output folder
    docx.Document(PROJECT_PAPER_TEMPLATE_PATH).save(OUTPUT_PATH)

    # open copied document
    document: docx.Document = docx.Document(OUTPUT_PATH)

    # process raw JSON data
    processed_data: airadaTypes.JSON_data = process_data(data)

    place_paragraphs_placeholders(document, processed_data)
    place_tables_placeholders(document, processed_data)

    replace_placeholders(document, processed_data)
    
    document.save(OUTPUT_PATH)
    
    return OUTPUT_PATH
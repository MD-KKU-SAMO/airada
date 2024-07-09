from datetime import datetime
from money import Money
from num_thai.thainumbers import NumThai

from airadaCore import airadaTypes

def get_numbered_list_text(*i: int, text: str) -> str:
    _number_text = ".".join(map(str, i))
    return f"{_number_text}. {text}"

def sum_money_str(items: list[airadaTypes.money_str]) -> str:
    _moneyItems: list[Money] = [Money(_, "THB") for _ in items]
    _sum: Money = sum(_moneyItems)

    return str(_sum.amount)

def get_money_thai_text(s: airadaTypes.money_str) -> str:
    if "." not in s:
        return f"{get_thai_number_text(int(s))}บาทถ้วน"
    
    _ = s.split(".")
    return f"{get_thai_number_text(int(_[0]))}บาท{get_thai_number_text(int(_[1]))}สตางค์"

def get_date_delta_thai_text(start: airadaTypes.date_str, end: airadaTypes.date_str) -> str:
    _start: datetime = datetime.fromisoformat(start)
    _end: datetime = datetime.fromisoformat(end)
    _delta: datetime = _end - _start
    return f"{_delta.days} วัน"

def get_thai_number_text(i: int) -> str:
    _nt: NumThai = NumThai()
    _: list[str] = _nt.NumberToTextThai(i)
    return "".join(_)

def toThaiDate(date: airadaTypes.date_str) -> str:
    # Use ISO 8601 format
    MONTH_TEXTS = [
        "มกราคม",
        "กุมภาพันธ์",
        "มีนาคม",
        "เมษายน",
        "พฤษภาคม",
        "มิถุนายน",
        "กรกฎาคม",
        "สิงหาคม",
        "กันยายน",
        "ตุลาคม",
        "พฤศจิกายน",
        "ธันวาคม"
    ]

    timeData: datetime = datetime.fromisoformat(date)
    thaiYear: int = timeData.year + 543
    monthText: str = MONTH_TEXTS[timeData.month - 1]
    
    return f"{timeData.day} {monthText} {thaiYear}"

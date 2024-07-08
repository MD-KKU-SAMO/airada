from datetime import datetime
from money import Money
from num_thai.thainumbers import NumThai

from airadaCore import airadaTypes 

def sum_money(items: list[str]) -> str:
    _moneyItems: list[Money] = [Money(_, "THB") for _ in items]
    _sum: Money = sum(_moneyItems)

    return str(_sum.amount)

def get_thai_money_text(s: airadaTypes.money_str) -> str:
    if "." not in s:
        return f"{intToThai(int(s))}บาทถ้วน"
    
    _ = s.split(".")
    return f"{intToThai(int(_[0]))}บาท{intToThai(int(_[1]))}สตางค์"

def get_duration_from_dates(start: airadaTypes.date_str, end: airadaTypes.date_str) -> str:
    _start: datetime = datetime.fromisoformat(start)
    _end: datetime = datetime.fromisoformat(end)
    _duration: datetime = _end - _start
    return f"{_duration.days} วัน"

def intToThai(i: int) -> str:
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
    monthText: int = MONTH_TEXTS[timeData.month - 1]
    return f"{timeData.day} {monthText} {thaiYear}"

from datetime import datetime
from money import Money
from num_thai.thainumbers import NumThai

from typing import Iterable, Any

from airadaCore.airadaTypes import MoneyStr, DateStr


def get_each(key, container) -> tuple[Any]:
    return tuple(_[key] for _ in container)


def to_numbered_list(container: Iterable[Iterable[str]]) -> tuple[str]:
    return tuple(get_numbered_list_text(i, text=_) for i, _ in enumerate(container, 1))


def each_to_numbered_list(key: Any, container: Iterable[Iterable[str]]) -> tuple[str]:
    return to_numbered_list(get_each(key, container))


def get_numbered_list_text(*i: int, text: str) -> str:
    _number_text = ".".join(map(str, i))
    return f"{_number_text}. {text}"


def sum_money_str(items: list[MoneyStr]) -> MoneyStr:
    _moneyItems: tuple[Money] = tuple(Money(_, "THB") for _ in items)
    _sum: Money = sum(_moneyItems)

    return str(_sum.amount)


def get_money_thai_text(s: MoneyStr) -> str:
    if "." not in s:
        return f"{get_thai_number_text(int(s))}บาทถ้วน"

    _ = s.split(".")
    return f"{get_thai_number_text(int(_[0]))}บาท{get_thai_number_text(int(_[1]))}สตางค์"


def get_date_delta_thai_text(start: DateStr, end: DateStr) -> str:
    _start: datetime = datetime.fromisoformat(start)
    _end: datetime = datetime.fromisoformat(end)
    _delta: datetime = _end - _start
    return f"{_delta.days} วัน"


def get_thai_number_text(i: int) -> str:
    _: list[str] = NumThai().NumberToTextThai(i)
    return "".join(_)


def toThaiDate(date: DateStr) -> str:
    # Use ISO 8601 format
    _MONTH_TEXTS = (
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
        "ธันวาคม",
    )

    _timeData: datetime = datetime.fromisoformat(date)
    _monthText: str = _MONTH_TEXTS[_timeData.month - 1]
    _thaiYear: int = _timeData.year + 543

    return f"{_timeData.day} {_monthText} {_thaiYear}"

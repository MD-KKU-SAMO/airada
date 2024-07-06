import datetime
import money
import num_thai.thainumbers

def moneySum(e: list[str]) -> str:
    return str(sum([money.Money(_, "THB") for _ in e]).amount)

def moneyToThai(moneyString: str) -> str:
    if "." not in moneyString:
        return f"{intToThai(moneyString)}บาทถ้วน"
    
    _ = moneyString.split(".")

    return f"{intToThai(int(_[0]))}บาท{intToThai(int(_[1]))}สตางค์"


def intToThai(i: int) -> str:
    num = num_thai.thainumbers.NumThai()
    return "".join(num.NumberToTextThai(i))

def toThaiDate(buffer: str) -> str:
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
    timeData = datetime.datetime.fromisoformat(buffer)
    thaiYear = str(timeData.year + 543)
    monthText = MONTH_TEXTS[timeData.month - 1]
    return f"{timeData.day} {monthText} {thaiYear}"

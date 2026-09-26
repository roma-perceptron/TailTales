EN2RU_STRFTIME = {
    # Дни недели (краткие)
    "Mon": "пн", "Tue": "вт", "Wed": "ср", "Thu": "чт", "Fri": "пт", "Sat": "сб", "Sun": "вс",
    # Месяцы (краткие)
    "Jan": "янв", "Feb": "фев", "Mar": "мар", "Apr": "апр", "May": "май", "Jun": "июн",
    "Jul": "июл", "Aug": "авг", "Sep": "сент", "Oct": "окт", "Nov": "ноя", "Dec": "дек"
}

def en2ru_strftime(date_str: str) -> str:
    # Заменяем английские слова на русские
    for eng, ru in EN2RU_STRFTIME.items():
        date_str = date_str.replace(eng, ru)
    return date_str


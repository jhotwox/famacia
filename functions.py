from customtkinter import CTkEntry
from datetime import datetime, timedelta
import pytz

def is_empty(text: str) -> bool:
    if len(text) <= 0: return True
    return False

def entry_empty(tx: CTkEntry, txt: str):
    if tx.get() == "":
        raise ValueError(f"Campo {txt} vacio")

def find_id(dictionary: dict, search_name: str) -> int | None:
    for id, name in dictionary.items():
        if name == search_name:
            return id
    return None

def is_numeric(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False

def is_alphabetic(text: str) -> bool:
    for character in text:
        if not (
            (ord('A') <= ord(character) <= ord('Z')) or
            (ord('a') <= ord(character) <= ord('z')) or
            (ord(character) == ord('á')) or
            (ord(character) == ord('é')) or
            (ord(character) == ord('í')) or
            (ord(character) == ord('ó')) or
            (ord(character) == ord('ú')) or
            (ord(character) == ord('Á')) or
            (ord(character) == ord('É')) or
            (ord(character) == ord('Í')) or
            (ord(character) == ord('Ó')) or
            (ord(character) == ord('Ú')) or
            (ord(character) == ord('ñ')) or
            (ord(character) == ord('Ñ')) or
            (ord(character) == ord(' '))
        ):
            return False
    return True

def clean_str(text: str) -> str:
    return text.lstrip().rstrip()

def get_datetime(days: int = 0) -> datetime:
    """Obtener la fecha actual en formato datetime

    :Example:
    >>> get_datetime()
        2024-09-30

    Returns:
        datetime: Fecha actual
    """
    
    date = datetime.now().astimezone(pytz.timezone('America/Mexico_City')).date()+timedelta(days=days)
    return date.strftime("%Y-%m-%d")
# print(get_datetime())

def get_date(days: int = 0) -> list[str]:
    """Obtener lista con la fecha actual

    :Example:
    >>> get_date()
        ['30', '12', '2021']

    Returns:
        list: [dia, mes, año]
    """
    
    today = get_datetime(days)
    return str(today).split('/')

def format_date_to_sql(date: str, _format: str = "%d/%m/%y") -> str:
    """Formatear la fecha a un formato valido para SQL

    :Example:
    >>> format_date_to_sql("01/07/24")
        2024-07-01
    >>> format_date_to_sql("2024-07-01", "%Y-%m-%d")
        2024-07-01
    Args:
        date (str): Fecha a formatear
        format (str) = "%d/%m/%y": Formato

    Returns:
        str: Fecha formateada
    """
    datetime_format: datetime = datetime.strptime(date, _format)
    return datetime_format.strftime("%Y-%m-%d")
# print(format_date_to_sql("01/07/24"))
# print(format_date_to_sql("2024-07-01", "%Y-%m-%d"))

def format_date_to_calendar(date: str, _format: str = "%Y-%m-%d") -> str:
    """Formatear la fecha a un formato valido para TKCalendar

    :Example:
    >>> format_date_to_calendar("2024-07-01")
        01-07-2024
    >>> format_date_to_calendar("2024/07/01", "%Y/%m/%d")
        01-07-2024
    Args:
        date (str): Fecha a formatear
        format (str): Formato

    Returns:
        str: Fecha formateada
    """
    datetime_format: datetime = datetime.strptime(date, _format)
    return datetime_format.strftime(f"%d/%m/%Y")

def get_column_from_list(list: list, column: int) -> list:
    """Obtener una columna de una lista

    :Example:
    >>> get_column_from_list([[1, 2], [3, 4], [5, 6]], 1)
        [2, 4, 6]
    >>> get_column_from_list([[1, 2], [3, 4], [5, 6]], 0)
        [1, 3, 5]

    Args:
        list (list): Lista a obtener la columna
        column (int): Columna a obtener

    Returns:
        list: Columna
    """
    return [row[column] for row in list]

def print_time():
    """Imprimir la hora actual

    :Example:
    >>> print_time()
        23:59:59
    """
    print(datetime.now().astimezone(pytz.timezone('America/Mexico_City')).time().strftime("%H:%M:%S"))
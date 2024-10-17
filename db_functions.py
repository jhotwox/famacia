import database as con
import mysql.connector

#region available
def is_available(value: str, table: str, column: str) -> bool | None:
    """Return a bool if the value wasn't used

    :Example:
    >>> is_available("cristian", "user", "name")
        True
    >>> is_available("cris", "user", "name")
        None and Exception
    
    Args:
        value (str): Value to search
        table (str): Name from the table to search
        column (str): Column where will gonna find

    Returns:
        bool | None: True if the value is available and None if the value isn't available or an error happened
        
    Raises:
        Exception: Value isn't available (Query returns False)
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT COUNT(*) AS available FROM {table} WHERE {column}='{value}'"
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.commit()
        if row[0] == 1:
            raise Exception(f"Value '{value}' isn't available")
        return True
    except mysql.connector.Error as err:
        print(f"[-] is_available SQL: {err}")
    except Exception as err:
        print(f"[-] is_available: {err}")
    finally:
        conn.close()
# print(is_available("nath", "user", "name"))


def name_available(value: str, table: str) -> bool | None:
    """Return a bool if the name is available

    :Example:
    >>> name_available("cristian", "user")
        True
    >>> name_available("cris", "user")
        None and Exception
    
    Args:
        value (str): Value to search
        table (str): Name of the table to search

    Returns:
        bool | None: True if the name is available and None if the name isn't available or an error happened
    
    Raises:
        Exception: Value isn't available (Query returns False)
    """
    return is_available(value, table, "name")
# print(name_available("crist", "user"))


def available_customers(user_id: int) -> dict:
    """Return a dictionary with the id and name of customers registered by the user
    
    :Example:
    >>> available_customers(1)
        {1: 'Gerson', 2: 'Karen', ...}

    Args:
        user_id (int): ID from the user
        
    Returns:
        dict: dictionary if table customer with columns name and id exist
    """
    
    name = get_column_with_user('customer', 'name', user_id)
    id = get_column_with_user('customer', 'id', user_id)
    return dict(zip(id, name))
# print(available_customers(1))


#region get column
def get_column_order_id(table: str, column: str) -> list | None:
    """Return the result of a query order by id
    
    :Example:
    >>> get_column_order_id('customer', "name")
        ['Gerson', 'Karen', ...]
    >>> get_column_order_id('unknown', "stock")
        None and Exception
        
    Args:
        table (str): Table to search 
        column (str): Column to search

    Raises:
        Exception: Column it's empty
        Exception: Table {db.table} doesn't exist

    Returns:
        list | None: Result of the column
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT {column} FROM {table} ORDER BY id"
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        rows = [item[0] for item in rows]
        if rows is None:
            raise Exception(f"Column '{column}' it's empty")
        return rows
    except mysql.connector.Error as err:
        print(f"[-] get_column SQL: {err}")
    except Exception as err:
        print(f"[-] get_column: {err}")
    finally:
        conn.close()


def get_column_with_user(table: str, column: str, user_id: int) -> list | None:
    """Return a column in form of list where the query contain the user_id and it's ordered by id
    
    :Example:
    >>> get_column_with_user('customer', "name", 1)
        ['Gerson', 'Karen', ...]
    >>> get_column_with_user('unknown', "stock", 3)
        None and Exception
        
    Args:
        table (str): Table to search 
        column (str): Column to search

    Raises:
        Exception: Column it's empty
        Exception: Table {db.table} doesn't exist

    Returns:
        list | None: Result of the column
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT {column} FROM {table} WHERE user_id = {user_id} ORDER BY id"
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        rows = [item[0] for item in rows]
        if rows is None:
            raise Exception(f"Column '{column}' it's empty")
        return rows
    except mysql.connector.Error as err:
        print(f"[-] get_column SQL: {err}")
    except Exception as err:
        print(f"[-] get_column: {err}")
    finally:
        conn.close()
# print(get_column_with_user('customer', "name", 1))


def get_columns(table: str, columns: str) -> list | None:
    """Return the result of the columns we want to had

    :Example:
    >>> get_columns('user', 'id, name')
        [(1, 'cris'), (2, 'criss'), ...]
    >>> get_columns('unknown', "stock")
        None and Exception
        
    Args:
        table (str): Name of the table
        columns (str): Name of the columns
        :Example:
        >>> "id, name, last_name"

    Raises:
        Exception: Columns {columns} are empty
        Exception: Table {db.table} doesn't exist
        Exception: Unknown column 'column' in 'field list'

    Returns:
        list | None: Result of the list
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT {columns} FROM {table}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        if rows is None:
            raise Exception(f"Columns '{columns}' are empty")
        return rows
    except mysql.connector.Error as err:
        print(f"[-] get_columns SQL: {err}")
    except Exception as err:
        print(f"[-] get_columns: {err}")
    finally:
        conn.close()
# print(get_columns('users', 'id, name'))


def get_column_with_stock(table: str, column: str) -> list | None:
    """Return the result of a query order by id and stock > 0
    
    :Example:
    >>> get_column_with_stock('part', "id")
        [1, 2, ...]
    >>> get_column_with_stock('unknown', "description")
        None and Exception
        
    Args:
        table (str): Table to search 
        column (str): Column to search

    Raises:
        Exception: Column it's empty
        Exception: Table {db.table} doesn't exist

    Returns:
        list | None: Result of the column
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT {column} FROM {table} WHERE stock > 0 ORDER BY id"
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.commit()
        rows = [item[0] for item in rows]
        if rows is None:
            raise Exception(f"Column '{column}' it's empty")
        return rows
    except mysql.connector.Error as err:
        print(f"[-] get_column SQL: {err}")
    except Exception as err:
        print(f"[-] get_column: {err}")
    finally:
        conn.close()
# print(get_column_with_stock('part', "id"))


#region search
def id_by_name(table: str, name: str) -> int | None:
    """Return the id corresponding to the name

    :Example:
    >>> id_by_name("customer", "Karen")
        4
    >>> id_by_name("customer", "Cris")
        None and Exception
        
    Args:
        table (str): Name of the table
        name (str): Name to search for

    Raises:
        Exception: {name} was not found in {table}
        Exception: Table {db.table} doesn't exist

    Returns:
        int | None: ID if the name was found and None if the name wasn't
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT id FROM {table} WHERE name = '{name}'"
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.commit()
        if row[0] is None:
            raise Exception(f"'{name}' wasn't found in '{table}'")
        return row[0]
    except mysql.connector.Error as err:
        print(f"[-] id_by_name SQL: {err}")
    except Exception as err:
        print(f"[-] id_by_name: {err}")
    finally:
        conn.close()
# print(id_by_name("customers", "cris"))


def name_by_id(table: str, id: int) -> str | None:
    """Return the name corresponding to the id

    :Example:
    >>> name_by_id("user", "1")
        "cris"
    >>> name_by_id("user", "4")
        None and Exception
        
    Args:
        table (str): Name of the table
        id (int): id to search for

    Raises:
        Exception: {id} was not found in {table}
        Exception: Table {db.table} doesn't exist

    Returns:
        str | None: Name if the id was found and None if the id wasn't
    """
    try:
        conn = con.conection().open()
        cursor = conn.cursor()
        sql = f"SELECT name FROM {table} WHERE id = {id}"
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.commit()
        if row[0] is None:
            raise Exception(f"'{id}' wasn't found in '{table}'")
        return row[0]
    except mysql.connector.Error as err:
        print(f"[-] name_by_id SQL: {err}")
    except Exception as err:
        print(f"[-] name_by_id: {err}")
    finally:
        conn.close()
# print(name_by_id("user", "4"))


def max_id(table: str) -> int | None:
    """Return the id from the AUTO_INCREMENT

    :Example:
    >>> max_id("customer")
        6
        
    Args:
        table (str): Name of the table

    Returns:
        int | None: id if the return was sucessful and None if the return was empty
    """
    
    conn = con.conection().open()
    cursor = conn.cursor()
    sql = f"SELECT MAX(id) FROM {table}"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row[0] is not None:
        return int(row[0])
    return None


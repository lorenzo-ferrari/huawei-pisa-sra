import sqlite3
import csv
import os

import constants

def init_db() -> None:
    if not os.path.isfile(constants.RESOURCES_PATH):
        print(f"An error occurred. Make sure file '{constants.RESOURCES_PATH}' exists.")
        return

    if os.path.isfile(constants.DB_PATH):
        os.remove(constants.DB_PATH)

    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    create_table_query = f"CREATE TABLE IF NOT EXISTS {constants.TABLE_NAME} ({constants.TABLE_FORMAT});"
    conn.execute(create_table_query)

    with open(constants.RESOURCES_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        insert_query = f"INSERT INTO {constants.TABLE_NAME} ({', '.join(header)}) VALUES ({', '.join(['?']*len(header))});"
        insert_data = [tuple(row) for row in csvreader]
        cursor.executemany(insert_query, insert_data)
    conn.commit()
    conn.close()

def lock(id) -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {constants.TABLE_NAME} SET state=? WHERE id=?", ('locked', id))
    conn.commit()
    conn.close()

def unlock(id) -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {constants.TABLE_NAME} SET state=? WHERE id=?", ('free', id))
    conn.commit()
    conn.close()

def ipById(id) -> str:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT location FROM {constants.TABLE_NAME} WHERE id=?", id)
    data = cursor.fetchall()
    conn.close()
    assert len(data) != 0
    ip = data[0][0]
    return ip

def cardinality() -> int:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(id) FROM {constants.TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()
    n = data[0][0]
    return n

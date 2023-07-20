import sqlite3
import csv
import os

import constants

def lock(conn, id) -> None:
    # conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {constants.TABLE_NAME} SET state=? WHERE id=?", ('locked', id))
    conn.commit()
    cursor.close()
    # conn.close()

def unlock(conn, id) -> None:
    # conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {constants.TABLE_NAME} SET state=? WHERE id=?", ('free', id))
    conn.commit()
    cursor.close()
    # conn.close()

def ipById(conn, resource_id) -> str:
    # conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT location FROM {constants.TABLE_NAME} WHERE id=?", str(resource_id))
    data = cursor.fetchall()
    cursor.close()
    # conn.close()
    assert len(data) != 0
    ip = data[0][0]
    return ip

def cardinality(conn) -> int:
    # conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(id) FROM {constants.TABLE_NAME}")
    data = cursor.fetchall()
    cursor.close()
    # conn.close()
    n = data[0][0]
    return n

def request_free_resource(conn, request_type, value) -> int:
    # conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    request_query = f"SELECT id FROM {constants.TABLE_NAME} WHERE state=='free' AND {request_type}='{value}'"
    cursor.execute(request_query)
    data = cursor.fetchall()
    cursor.close()
    # conn.close()
    if len(data) == 0:
        return constants.ID_NOT_FOUND
    else:
        resource_id = data[0][0]
        return resource_id

def candidates_resources(conn, request_type, value):
    # conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    request_query = f"SELECT id FROM {constants.TABLE_NAME} WHERE {request_type}='{value}'"
    cursor.execute(request_query)
    data = cursor.fetchall()
    cursor.close()
    # conn.close()
    return [int(x[0]) for x in data]

#!/bin/python

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

if __name__=='__main__':
    init_db()

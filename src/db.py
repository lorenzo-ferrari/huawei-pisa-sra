import sqlite3
import csv

import constants

def init_db() -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()

    create_table_query = f"CREATE TABLE IF NOT EXISTS {constants.TABLE_NAME} ({constants.constants.TABLE_FORMAT});"
    conn.execute(create_table_query)

    try:
        with open(constants.RESOURCES_PATH, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            insert_query = f"INSERT INTO {constants.TABLE_NAME} ({', '.join(header)}) VALUES ({', '.join(['?']*len(header))});"
            insert_data = [tuple(row) for row in csvreader]
            cursor.executemany(insert_query, insert_data)
    except:
        print(f"Something went wrong...\nTry removing '{constants.DB_PATH}' and make sure '{constants.RESOURCES_PATH}' exists")

    conn.commit()
    conn.close()

# prints the database
def print_db() -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {constants.TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()

    print(f"{constants.TABLE_NAME}:")
    for row in data:
        print(row)

def lock(id) -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()

    print(f'Locking resource with id={id}')
    cursor.execute(f"UPDATE {constants.TABLE_NAME} SET state=? WHERE id=?", ('locked', id))

    conn.commit()
    conn.close()

def unlock(id) -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()

    print(f'Unlocking resource with id={id}')
    cursor.execute(f"UPDATE {constants.TABLE_NAME} SET state=? WHERE id=?", ('free', id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print_db()
    # request('id', '1')
    lock(1)
    print_db()
    unlock(1)
    print_db()

import sqlite3
import csv

DB_PATH='resources.db'
RESOURCES_PATH='../input/resources.csv'
TABLE_FORMAT = 'id TEXT PRIMARY KEY, name TEXT, location TEXT, model TEXT, state TEXT'
TABLE_NAME = 'main_table'

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_table_query = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({TABLE_FORMAT});"
    conn.execute(create_table_query)

    try:
        with open(RESOURCES_PATH, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            insert_query = f"INSERT INTO {TABLE_NAME} ({', '.join(header)}) VALUES ({', '.join(['?']*len(header))});"
            insert_data = [tuple(row) for row in csvreader]
            cursor.executemany(insert_query, insert_data)
    except:
        print(f"Something went wrong...\nTry removing '{DB_PATH}' and make sure '{RESOURCES_PATH}' exists")
        return

    conn.commit()
    conn.close()

def print_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()

    print(f"{TABLE_NAME}:")
    for row in data:
        print(row)

# returns the id of a free resource of the requested type, -1 if there are none
def request(request_type, value) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    request_query = f"SELECT * FROM {TABLE_NAME} WHERE state=='free' AND {request_type}='{value}'"
    # print(request_query)
    cursor.execute(request_query)

    data = cursor.fetchall()
    conn.close()
    
    if len(data) == 0:
        return -1

    lock(data[0][0])
    return data[0]

    print(f"request result:")
    for row in data:
        print(row)

def lock(id) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f'Locking resource with id={id}')
    cursor.execute(f"UPDATE {TABLE_NAME} SET state=? WHERE id=?", ('locked', id))

    conn.commit()
    conn.close()

def unlock(id) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(f'Unlocking resource with id={id}')
    cursor.execute(f"UPDATE {TABLE_NAME} SET state=? WHERE id=?", ('free', id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print_db()
    # request('id', '1')
    lock(2)
    print_db()
    unlock(2)
    print_db()

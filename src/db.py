import sqlite3
import csv

DB_PATH='resources.db'
RESOURCES_PATH='../input/resources.csv'
TABLE_FORMAT = 'id INT PRIMARY KEY, name TEXT, location TEXT, model TEXT, state TEXT'
TABLE_NAME = 'main_table'

def main():
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

def print_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()

    for row in data:
        print(row)

if __name__ == '__main__':
    main()
    print_db()

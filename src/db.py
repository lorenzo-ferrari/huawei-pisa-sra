import sqlite3
import csv

DB_PATH='resources.db'
RESOURCES_PATH='../input/resources.csv'
TABLE_FORMAT = 'id TEXT PRIMARY KEY, name TEXT, location TEXT, model TEXT'

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    create_table_query = f"CREATE TABLE IF NOT EXISTS main_table ({TABLE_FORMAT});"
    conn.execute(create_table_query)

    with open(RESOURCES_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        print(header)
        insert_query = f"INSERT INTO main_table ({', '.join(header)}) VALUES ({', '.join(['?']*len(header))});"
        insert_data = [tuple(row) for row in csvreader]
        print(insert_data)
        cursor.executemany(insert_query, insert_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()

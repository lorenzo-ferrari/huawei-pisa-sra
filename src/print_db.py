import sqlite3

import constants

def print_db() -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {constants.TABLE_NAME}")
    data = cursor.fetchall()
    conn.close()
    print(f"{constants.TABLE_NAME}:")
    for row in data:
        print(row)

if __name__=='__main__':
    print_db()

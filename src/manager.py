import sqlite3
import csv

import db
import constants

# returns the ip of a free resource of the requested type, -1 if there are none
def request_db(request_type, value) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    request_query = f"SELECT id,location FROM {constants.TABLE_NAME} WHERE state=='free' AND {request_type}='{value}'"
    print(request_query)
    cursor.execute(request_query)

    data = cursor.fetchall()

    conn.close()
    
    if len(data) == 0:
        return "-1"
    else:
        resource_id, resource_ip = data[0]
        db.lock(resource_id)
        return resource_ip

# currently do nothing
def handle_request(user_id, request_type, value, prio, timeout):
    pass

def run_simulation():
    # currently do nothing
    print('Running simulation...')
    with open(constants.REQUESTS_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        next(csvreader)
        for row in csvreader:
            print(row)

def main():
    # request_db('id', 2)
    run_simulation()

if __name__=='__main__':
    main()

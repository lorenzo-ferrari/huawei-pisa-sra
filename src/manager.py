import sqlite3

import db
from constants import *

# returns the ip of a free resource of the requested type, -1 if there are none
def request_db(request_type, value) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    request_query = f"SELECT id,location FROM {TABLE_NAME} WHERE state=='free' AND {request_type}='{value}'"
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

if __name__=='__main__':
    request_db('id', 2)

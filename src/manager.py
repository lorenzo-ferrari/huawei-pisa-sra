import sqlite3
import csv
import heapq

import db
import constants

class Event:
    def __init__(self, timestamp, user_id, request_type, value, prio, timeout = -1):
        self.timestamp = timestamp
        self.user_id = user_id
        self.request_type = request_type
        self.value = value
        self.prio = prio
        self.timeout = timeout

    def __lt__(self, oth):
        return (int(self.timestamp), int(self.timeout)) < (int(oth.timestamp), int(oth.timeout))

class CustomQueue:
    def __init__(self):
        self.q = []
    def push(self, event : Event) -> None :
        heapq.heappush(self.q, event)
    def pop(self) -> Event:
        element = heapq.heappop(self.q)
        return element
    def empty(self) -> bool:
        return len(self.q) == 0

q = CustomQueue()

# returns the id of a free resource of the requested type, -1 if there are none
def request_db(request_type, value) -> int:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()

    request_query = f"SELECT id,location FROM {constants.TABLE_NAME} WHERE state=='free' AND {request_type}='{value}'"
    cursor.execute(request_query)

    data = cursor.fetchall()

    conn.close()
    
    if len(data) == 0:
        return -1
    else:
        resource_id, resource_ip = data[0]
        return resource_id

def handle_event(event):
    if event.timeout == -1:
        assert event.request_type == "id"
        db.unlock(event.value)
        print(f'Timestamp {event.timestamp} : user {event.user_id} freed the resource with id {event.value}')
    else:
        resource_id = request_db(event.request_type, event.value)
        print(f'Timestamp {event.timestamp} : user {event.user_id} requested a resource with "{event.request_type}":"{event.value}"')
        if resource_id == -1:
            print(f'\trequest denied')
        else:
            resource_ip = db.ipById(resource_id)
            db.lock(resource_id)
            print(f'\trequest accepted: user {event.user_id} obtained access to ip {resource_ip}')
            q.push(Event(event.timestamp + event.timeout, event.user_id, "id", resource_id, event.prio, -1))

def run_simulation():
    # currently do nothing
    print('Running simulation...')
    with open(constants.REQUESTS_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        next(csvreader)
        global q
        for row in csvreader:
            print(row)
            (timestamp, user_id, request_type, value, prio, timeout) = row
            q.push(Event(timestamp, user_id, request_type, value, prio, timeout))

        while not q.empty():
            event = q.pop()
            handle_event(event)

def main():
    # request_db('id', 2)
    run_simulation()


if __name__=='__main__':
    main()

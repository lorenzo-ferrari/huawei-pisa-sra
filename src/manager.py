import sqlite3
import csv
import heapq
import logging

import db
import constants

logging.basicConfig(filename='../log.txt', filemode='a', format='%(message)s', level=logging.INFO)

class Event:
    def __init__(self, timestamp, user_id, request_type, value, prio, timeout):
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
timer = 0

def request_db(request_type, value) -> int:
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()

    request_query = f"SELECT id FROM {constants.TABLE_NAME} WHERE state=='free' AND {request_type}='{value}'"
    cursor.execute(request_query)

    data = cursor.fetchall()

    conn.close()
    
    if len(data) == 0:
        return -1
    else:
        resource_id = data[0][0]
        return resource_id

def handle_event(event):
    global timer
    timer = event.timestamp
    print(f'timestamp: {event.timestamp}')
    print(f'timeout: {event.timeout}')

    if event.timeout == -1:
        assert event.request_type == "id"
        db.unlock(event.value)
        logging.info(f'[.] Timestamp {timer} - user {event.user_id} freed the resource with id {event.value}')
    else:
        resource_id = request_db(event.request_type, event.value)
        logging.info(f'[?] Timestamp {timer} - user {event.user_id} requested a resource with "{event.request_type}":"{event.value}"')
        if resource_id == -1:
            logging.info(f'[-] Timestamp {timer} - request denied')
        else:
            resource_ip = db.ipById(resource_id)
            db.lock(resource_id)
            logging.info(f'[+] Timestamp {timer} - request accepted : user {event.user_id} obtained access to ip {resource_ip} for up to {event.timeout} seconds')
            q.push(Event(int(event.timestamp) + int(event.timeout), event.user_id, "id", resource_id, event.prio, -1))

def run_simulation():
    with open(constants.REQUESTS_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        next(csvreader)
        global q
        for row in csvreader:
            (timestamp, user_id, request_type, value, prio, timeout) = row
            q.push(Event(timestamp, user_id, request_type, value, prio, timeout))

        while not q.empty():
            event = q.pop()
            handle_event(event)

def main():
    run_simulation()

if __name__=='__main__':
    main()

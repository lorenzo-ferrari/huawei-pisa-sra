import sqlite3
import csv
import heapq
import logging

import db
import constants

logging.basicConfig(filename='../log.txt', filemode='w', format='%(message)s', level=logging.INFO)

class Event:
    def __init__(self, timestamp, request_id, user_id, request_type, value, prio, timeout):
        self.timestamp = timestamp
        self.request_id = request_id
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

eventsQ = CustomQueue()
timer = 0
cur_request_id = 0
is_satisfied = []
queues = []

def new_request_id() -> int:
    global is_satisfied
    global cur_request_id
    is_satisfied.append(False)
    ret = cur_request_id
    cur_request_id += 1
    return ret

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

def candidates_resources(request_type, value):
    conn = sqlite3.connect(constants.DB_PATH)
    cursor = conn.cursor()
    request_query = f"SELECT id FROM {constants.TABLE_NAME} WHERE {request_type}='{value}'"
    cursor.execute(request_query)
    data = cursor.fetchall()
    conn.close()
    return [int(x[0]) for x in data]

def handle_event(event) -> None:
    global timer
    global eventsQ
    global queues
    timer = event.timestamp

    if event.timeout == -1:
        assert event.request_type == "id"
        id = int(event.value)
        db.unlock(event.value)
        logging.info(f'[.] Timestamp {timer} - user {event.user_id} freed the resource with id {id}')

        # check for people in queue
        while not queues[id].empty():
            req = queues[id].pop()
            if is_satisfied[req.request_id]:
                continue
            else:
                req.timestamp = timer
                eventsQ.push(req)
                break
    elif is_satisfied[event.request_id]:
        return
    else:
        resource_id = request_db(event.request_type, event.value)
        logging.info(f'[?] Timestamp {timer} - user {event.user_id} requested a resource with "{event.request_type}":"{event.value}"')
        if resource_id == -1:
            logging.info(f'[-] Timestamp {timer} - request denied')
            possible_ids = candidates_resources(event.request_type, event.value)
            for i in possible_ids:
                queues[i].push(event)
        else:
            resource_ip = db.ipById(resource_id)
            db.lock(resource_id)
            is_satisfied[event.request_id] = True
            logging.info(f'[+] Timestamp {timer} - request accepted : user {event.user_id} obtained access to ip {resource_ip} for up to {event.timeout} seconds')
            eventsQ.push(Event(int(event.timestamp) + int(event.timeout), -1, event.user_id, "id", resource_id, event.prio, -1))

def online_request(user_id, request_type, value, prio, timeout = 7200) -> None: # max timeout: 2h
    is_satisfied.append('False')
    handle_event(Event(timer, new_request_id, user_id, request_type, value, prio, timeout))

def online_free(user_id, request_type, value, prio) -> None:
    handle_event(Event(timer, -1, user_id, request_type, value, prio, -1))

def run_simulation() -> None:
    with open(constants.REQUESTS_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        global eventsQ
        for row in csvreader:
            (timestamp, user_id, request_type, value, prio, timeout) = row
            is_satisfied.append('False')
            eventsQ.push(Event(timestamp, new_request_id(), user_id, request_type, value, prio, timeout))

        while not eventsQ.empty():
            event = eventsQ.pop()
            handle_event(event)

def main():
    global queues
    queues = [CustomQueue() for _ in range(db.cardinality() + 1)]

    run_simulation()

    # db.print_db()
    # online_request('Lorenzo', 'id', 1, 'low')
    # db.print_db()
    # online_free('Lorenzo', 'id', 1, 'low')
    # db.print_db()
    # online_free('Lorenzo', 'id', 1, 'low')

if __name__=='__main__':
    main()

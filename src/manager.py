import sqlite3
import csv
import heapq
import logging
import time

import db
import constants

logging.basicConfig(filename='../log.txt', filemode='w', format='%(message)s', level=logging.INFO)

class RequestEvent:
    def __init__(self, timestamp, request_id, user_id, timeout): # todo, add priorities
        self.timestamp = timestamp
        self.request_id = request_id
        self.user_id = user_id
        self.timeout = timeout

    def __lt__(self, oth):
        # in the future, take into account priorities
        return self.timestamp < oth.timestamp

class FreeEvent:
    def __init__(self, timestamp, user_id, resource_id):
        self.timestamp = timestamp
        self.user_id = user_id
        self.resource_id = resource_id

    def __lt__(self, oth):
        return self.timestamp < oth.timestamp

class CustomQueue:
    def __init__(self):
        self.q = []
    def push(self, event) -> None :
        heapq.heappush(self.q, event)
    def top(self):
        return self.q[0]
    def pop(self):
        element = heapq.heappop(self.q)
        return element
    def empty(self) -> bool:
        return len(self.q) == 0

class State:
    def __init__(self, state):
        self.eventsQ = state.eventsQ
        self.timer = state.timer
        self.cur_request_id = state.cur_request_id
        self.is_satisfied = state.is_statisfied
        self.queues = state.queues

    def __init__(self):
        self.eventsQ = CustomQueue()
        self.timer = 0
        self.cur_request_id = 0
        self.is_satisfied = []
        self.queues = []

    def new_request_id(self) -> int:
        self.is_satisfied.append(False)
        ret = self.cur_request_id
        self.cur_request_id += 1
        return ret
    
state = State()

def online_request(timestamp, user_id, request_type, value, timeout = constants.MAX_TIMEOUT) -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    offline_request(conn, timestamp, user_id, request_type, value, timeout)
    conn.close()

def online_free(user_id, resource_id) -> None:
    conn = sqlite3.connect(constants.DB_PATH)
    offline_free(conn, user_id, resource_id)
    conn.close()

def offline_request(conn, timestamp, user_id, request_type, value, timeout) -> None:
    global state # in the future, load state from file
    state.timer = timestamp

    free_expired_assignments(conn)

    logging.info(f'[?] Timestamp {state.timer} - user {user_id} requested a resource with "{request_type}":"{value}"')
    request_id = state.new_request_id()
    resource_id = db.request_free_resource(conn, request_type, value)

    if resource_id == constants.ID_NOT_FOUND:
        logging.info(f'[-] Timestamp {state.timer} - request currently denied: queueing...')
        possible_ids = db.candidates_resources(conn, request_type, value)
        for id in possible_ids:
            state.queues[id].push(RequestEvent(timestamp, request_id, user_id, timeout))
    else:
        resource_ip = db.ipById(conn, resource_id)
        db.lock(conn, resource_id)
        state.is_satisfied[request_id] = True
        logging.info(f'[+] Timestamp {state.timer} - request accepted : user {user_id} obtained access to ip {resource_ip} for up to {timeout} seconds')
        state.eventsQ.push(FreeEvent(int(state.timer) + int(timeout), user_id, resource_id))


def offline_free(conn, user_id, resource_id) -> None:
    db.unlock(conn, int(resource_id))
    logging.info(f'[.] Timestamp {state.timer} - user {user_id} freed the resource with id {resource_id}')

    check_resource_queue(conn, int(resource_id))

def check_resource_queue(conn, resource_id):
    # check for users waiting for resource `resource_id`
    while not state.queues[int(resource_id)].empty():
        req = state.queues[int(resource_id)].pop()
        if state.is_satisfied[int(req.request_id)]:
            continue
        else:
            db.lock(conn, int(resource_id))
            offline_request(conn, state.timer, req.user_id, "id", resource_id, timeout = req.timeout)
            resource_ip = db.ipById(conn, resource_id)
            logging.info(f'[+] Timestamp {state.timer} - user {req.user_id} (queueing) obtained access to ip {resource_ip} for up to {req.timeout} seconds')
            state.eventsQ.push(FreeEvent(int(state.timer) + int(req.timeout), req.user_id, resource_id))
            break

def free_expired_assignments(conn) -> None:
    while not state.eventsQ.empty() and state.eventsQ.top().timestamp <= int(state.timer):
        event = state.eventsQ.pop()
        offline_free(conn, event.user_id, event.resource_id)

def run_simulation() -> None:
    with open(constants.REQUESTS_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        global state
        for row in csvreader:
            (timestamp, user_id, request_type, value, prio, timeout) = row
            state.timer = timestamp
            online_request(timestamp, user_id, request_type, value, timeout)

def main():
    # init manager
    conn = sqlite3.connect(constants.DB_PATH)
    global state
    state.queues = [CustomQueue() for _ in range(db.cardinality(conn) + 1)]
    conn.close()

    run_simulation()

if __name__=='__main__':
    main()

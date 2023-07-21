import csv
import time

import manager
import constants

def run_simulation() -> None:
    with open(constants.REQUESTS_PATH, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        global state
        for row in csvreader:
            (timestamp, user_id, request_type, value, prio, timeout) = row
            manager.online_request(timestamp, user_id, request_type, value, timeout)

def main():
    run_simulation()

if __name__=='__main__':
    main()

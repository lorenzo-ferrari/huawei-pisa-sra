#!/bin/python

import time
import logging

import manager
import constants

def main():
    logging.basicConfig(filename=constants.LOG_PATH, filemode='a', format='%(message)s', level=logging.INFO)

    timestamp = int(time.time())
    user_id = input("Enter your user_id: ")
    request_type,value = input("Enter the kind of resource you need (example: 'model TC397XE'): ").split()
    timeout = int(input("Enter a timeout (in seconds) after which your resource will automatically be freed: "))

    outcome = manager.online_request(timestamp, user_id, request_type, value, timeout)
    if outcome:
        print("Success")
    else:
        print("Currently denied")

if __name__=='__main__':
    main()

import logging

import manager
import constants

def main():
    logging.basicConfig(filename=constants.LOG_PATH, filemode='a', format='%(message)s', level=logging.INFO)

    user_id = input("Enter your user_id")
    request_type,value = input("Enter the kind of resource you are freeing (example: 'model TC397XE'): ").split()

    manager.online_free(user_id, request_type, value)

if __name__=='__main__':
    main()

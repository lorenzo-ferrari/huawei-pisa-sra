RESOURCES_PATH='../input/resources.csv'
REQUESTS_PATH='../input/requests.csv'

DB_PATH='resources.db'
TABLE_FORMAT = 'id TEXT PRIMARY KEY, name TEXT, location TEXT, model TEXT, state TEXT'
TABLE_NAME = 'main_table'

MAX_TIMEOUT = 7200
ID_NOT_FOUND = -1
NULL_REQUEST_ID = -1

FREE_EVENT_TYPE = 'FREE'
REQUEST_EVENT_TYPE = 'REQUEST'

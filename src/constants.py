RESOURCES_PATH='../input/resources.csv'
REQUESTS_PATH='../input/requests.csv'
DB_PATH='resources.sqlite'
STATE_PATH = 'state_obj.pickle'

TABLE_FORMAT = 'id TEXT PRIMARY KEY, name TEXT, location TEXT, model TEXT, state TEXT'
TABLE_NAME = 'resources_table'

MAX_TIMEOUT = 7200
ID_NOT_FOUND = -1

from pathlib import Path

BOT_TOKEN = ''
BASE_URL = ''  # Webhook domain
WEBHOOK_PATH = f''
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'

LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')

admins = []

ip = {
    'db': ''
}

mysql_info = {
    'host':     ip['db'],
    'user':     '',
    'password': '',
    'db':       '',
    'maxsize':  5,
    'port':     3306
}

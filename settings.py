from bestconfig import Config

import re
import logging
import logging.config
import logging.handlers



root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

config = Config()
bot_token = config.get('BOT_TOKEN')
api_id = config.get("API_ID")
api_hash = config.get("API_HASH")

server_url = config.get("HOST.IMAGE_CHECK_SERVER")
server_token = config.get("SERVER_TOKEN")

coefficient_unsafe = config.get("COEFFICIENT.UNSAFE")

regex_str = """http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""

link_regex = re.compile(regex_str, re.DOTALL)

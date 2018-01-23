from dashlogger import Logger
from config_handler import setup_store

logger = Logger("log")

# Setup the config store
setup_store(logger)
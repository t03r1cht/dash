from dashlogger import Logger
import config_handler
from werkzeug.security import generate_password_hash, check_password_hash

print(config_handler.check_config_entry("role_id-board-administrator", "0", check_values=True))
print(config_handler.get_config_entry("role_id-board-administrator"))

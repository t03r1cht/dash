from dashlogger import Logger
import config_handler
from werkzeug.security import generate_password_hash, check_password_hash
import json

d = {"val": "bla", "abc": "def", "list": {
    "nested1": "hallo",
    "nested2": "hallooo",
    "another_list": {
        "bla": "blub",
        "nested_item": "ok"
    }
}}

x = json.dumps(d, ensure_ascii=False)
# print(json.dumps(d, ensure_ascii=False))
#
# print(d["list"]["nested2"])
# print(d["list"]["another_list"]["nested_item"])

print(json.loads(x)["list"]["another_list"]["nested_item"])

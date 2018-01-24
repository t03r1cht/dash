import sqlite3
import datetime


def setup_store(logger):
    with sqlite3.connect("config-store.db") as conn:
        try:
            conn.execute("CREATE TABLE configs (id INTEGER PRIMARY KEY, name TEXT UNIQUE , value TEXT)")

            """
            Creation date of the config store.
            """
            conn.execute("INSERT INTO configs (name, value) VALUES (?, ?)", ("created-at", datetime.datetime.now(),))

            """
            Index mode of the board.
            
            - login-required: Prompts the user to login when trying to visit the board
            - login-for-access: Allows the user to browse through the board with read-only access. User needs to login to post data.
            """
            conn.execute("INSERT INTO configs (name, value) VALUES (?, ?)", ("board-access-mode", "login-for-access",))

            """
            Role IDs for the different board roles.
            Default:
            - 0: Board Administrator
            - 1: Board Moderator
            - 2: Board Member (verified)
            - 3: Board Member (not verified, verification pending)
            """
            conn.execute("INSERT INTO configs (name, value) VALUES (?, ?)", ("role_id-board-administrator", "0",))

        except sqlite3.OperationalError as e:
            logger.error("Error: Database was already created. You can reset it with the '-r' option.\n" + str(e))
    print("Config store setup complete...\n")


def check_config_entry(key, check_value, check_values=False):
    with sqlite3.connect("config-store.db") as conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT name, value FROM configs WHERE name = ?", (key,))

            data = cursor.fetchone()

            if len(data) == 0:
                if not check_values:
                    return None
                else:
                    return False

        except Exception as e:
            if not check_values:
                return None
            else:
                return False

        if not check_values:
            return data[1]
        else:
            return data[1] == check_value


def get_config_entry(key):
    with sqlite3.connect("config-store.db") as conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT name, value FROM configs WHERE name = ?", (key,))

            data = cursor.fetchone()

            if len(data) == 0:
                return -1

        except Exception as e:
            return -1

        return data[1]

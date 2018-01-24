from flask import Flask
from flaskext.mysql import MySQL
import datetime


class DB_Handler:
    DB_TABLE_USERS = "dash_users"

    def connect_to_db(self, mysql):
        conn = mysql.connect()
        cursor = conn.cursor()

        print("db conn ok")

        conn.close()

    def check_for_user_existence(self, mysql, email):
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, email, password, uid, role_id FROM " + self.DB_TABLE_USERS + " WHERE email = %s",
            (email,))

        data = cursor.fetchone()

        if cursor.rowcount == 0:
            conn.close()
            return None

        conn.close()

        return {"username": str(data[0]), "email": str(data[1]), "password": str(data[2]), "uid": str(data[3]),
                "role_id": data[4]}

    def add_new_user(self, mysql, user_data):
        """
        Add a new user to the users table.
        Return None if the user already exists.
        Return False if the user was not added due to a raised exception.
        Return the user dict that was added.
        """
        conn = mysql.connect()
        cursor = conn.cursor()

        # Check if the user already exists
        print("email=" + str(user_data["email"]))
        cursor.execute(
            "SELECT username, email, password, uid, role_id FROM " + self.DB_TABLE_USERS + " WHERE email = %s",
            (str(user_data["email"]),))

        user_record = cursor.fetchone()
        if user_record is None:
            print("user already exists")
            return None

        # role_id = 3: Board Member (not verified)
        role_id = 3
        creation_date = datetime.datetime.now()
        profile_data = "to_be_created"

        user_data["creation_date"] = creation_date
        user_data["role_id"] = role_id
        user_data["profile_data"] = profile_data

        try:
            cursor.execute(
                "INSERT INTO " + self.DB_TABLE_USERS + " (username, email, password, creation_date, role_id, profile_data) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_data["username"],
                 user_data["email"],
                 user_data["password"],
                 user_data["creation_date"],
                 user_data["role_id"],
                 user_data["profile_data"]
                 ))

            cursor.commit()
            conn.close()
            return user_data

        except Exception as e:
            conn.close()
            print("error=add_new_user:\n" + str(e))
            return False

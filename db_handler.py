from flask import Flask
from flaskext.mysql import MySQL
import datetime
import json


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

        cursor.callproc("dash_board_db.check_for_user_existence", (email,))

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
        user_record = self.check_for_user_existence(mysql, user_data["email"])
        if user_record is not None:
            print("user already exists")
            return None, None

        # role_id = 3: Board Member (not verified)
        role_id = 3
        creation_date = datetime.datetime.now()
        profile_data = "to_be_created"

        user_data["creation_date"] = creation_date
        user_data["role_id"] = role_id
        user_data["profile_data"] = profile_data

        try:
            cursor.callproc("dash_board_db.add_new_user", (user_data["username"],
                                                           user_data["email"],
                                                           user_data["password"],
                                                           user_data["creation_date"],
                                                           user_data["role_id"],
                                                           user_data["profile_data"]))
            conn.commit()
            conn.close()
            return user_data, None

        except Exception as e:
            conn.close()
            print("error=add_new_user:\n" + str(e))
            return False, e

    def get_section_list(self, mysql):
        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            cursor.callproc("dash_board_db.get_section_list")

            data = cursor.fetchall()

            if cursor.rowcount == 0:
                conn.close()
                return None

            conn.close
            return data
        except Exception as e:
            conn.close()
            return None

    def get_subsections_for_section_id(self, mysql, section_id):
        conn = mysql.connect()
        cursor = conn.cursor()

        try:
            cursor.callproc("get_subsections_for_section_id", (section_id,))

            data = cursor.fetchall()

            if cursor.rowcount == 0:
                conn.close()
                return None

            conn.close()
            return data

        except Exception as e:
            conn.close()
            return None

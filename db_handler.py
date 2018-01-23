from flask import Flask
from flaskext.mysql import MySQL


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

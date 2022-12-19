import sqlite3
from contextlib import closing
import psycopg2


class BaseConnect:

    def __init__(self):
        self.con = psycopg2.connect(
            database="Nails",
            user="postgres",
            password="111",
            host="127.0.0.1",
            port="1503"
        )
        print("ok")


    def add_user(self, name):
        with closing(sqlite3.connect('users.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            # cur = connection.cursor()

            cur.execute("INSERT INTO users VALUES(NULL, ?)", (name))
            connection.commit()
        # connection.close()

    def delete_user(self):
        with closing(sqlite3.connect('users.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            # cur = connection.cursor()
            cur.execute("DELETE FROM users WHERE id > '600'")
            connection.commit()
        # connection = sqlite3.connect('users.db')
        # cur = connection.cursor()
        # cur.execute("DELETE FROM users WHERE id > '600'")
        # connection.commit()
        # connection.close()

    def find_user_by_name(self, name):

        # connection = sqlite3.connect('users.db')
        # cur = connection.cursor()
        with closing(sqlite3.connect('users.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            result = None
            for row in cur.execute("select id, name from users where name = :name", {"name": name}):
                result = row[0]
                # connection.close()
            return result

    def find_user_by_id(self, id):
        with closing(sqlite3.connect('users.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            # connection = sqlite3.connect('users.db')
            # cur = connection.cursor()
            result = None
            for row in cur.execute("select id, name from users where id = :id", {"id": id}):
                result = row[1]
            # connection.close()
            return result

    def find_near_time(self):
        with closing(sqlite3.connect('sign_in.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            # connection = sqlite3.connect('sign_in.db')
            # cur = connection.cursor()
            result = []
            for row in cur.execute(
                    "SELECT month, day, time, id, (min(month) AND min(day)) FROM sign_in WHERE id is NULL"):
                result = row
                # connection.close()
            print(result)
            return result

    def check_date(self, month, day):
        with closing(sqlite3.connect('sign_in.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            # connection = sqlite3.connect('sign_in.db')
            # cur = connection.cursor()
            result = []
            for row in cur.execute(
                    "SELECT time FROM sign_in WHERE (month = :month AND day = :day and id is NULL)",
                    {"month": int(month), "day": int(day)}):
                result.append(row)
            # connection.close()
            # arr = []
            print(result)
            # for i in result:
            #     print(i)
            #     arr.append(str(i))
            return result

    def sing_up(self, month, day, time, id):
        with closing(sqlite3.connect('sign_in.db')) as connection:
            # connection = sqlite3.connect('users.db')
            cur = connection.cursor()
            # connection = sqlite3.connect('sign_in.db')
            # cur = connection.cursor()
            line = "UPDATE sign_in SET id = '" + str(id) + "' WHERE day = '" + str(day) + "' and month = '" + str(
                month) + "' and time = '" + str(time) + "'"
            for row in cur.execute(line):
                print("check")
            connection.commit()
    # connection.close()

'''
@File       :   db_op.py
@Time       :   9/27/2020
@Author     :   Eric Jin
@Version    :   2.0
@Contact    :   jyseric@126.com
@License    :   WTFPL
'''


import sqlite3

# DATABASE STRUCTURE
# ALL_USER Table:
#   ID INT PRIMARY KEY NOT NULL,
#   USERNAME TEXT NOT NULL,
#   PASSWD CHAR(50) NOT NULL,
#   LOGIN_STATUS BOOLEAN NOT NULL,
#
#
# MSG"USERID" Table:
#   SENDER_ID INT, // IF NULL THEN USER IS THE SENDER
#   TIME TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   MSG TEXT NOT NULL,
#
# FRIEND_LIST"USERID" Table:
#   FRIEND_ID INT NOT NULL,
#
# FRIEND_REQUEST"USERID" Table:
#   FRIEND_ID INT NOT NULL,
#   REQ_NOTE TEXT,

# TODO `TEXT` in DB do not support '


class dbOp:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # ========== ALL User Table ==========

    def create_allusertable(self):
        self.cursor.execute(
            """
                CREATE TABLE AUT
                (
                    ID INT PRIMARY KEY NOT NULL,
                    USERNAME TEXT NOT NULL,
                    PASSWD CHAR(50) NOT NULL,
                    LOGIN_STATUS BOOLEAN NOT NULL
                )
            """
        )
        self.conn.commit()

    def insert_allusertable(self, user_id, user_name, passwd, login_status):
        self.cursor.execute(
            """
                INSERT INTO AUT (ID, USERNAME, PASSWD, LOGIN_STATUS) 
                VALUES ({}, '{}', '{}', {})
            """.format(user_id, user_name, passwd, login_status)
        )
        self.conn.commit()
        print("insert into all user table")
        return 1

    def get_max_userid(self):
        data = self.cursor.execute("SELECT MAX(ID) from AUT")
        for row in data:
            return row[0]

    def delete_allusertable(self, user_id):
        self.cursor.execute("DELETE from AUT where ID={}".format(user_id))
        self.conn.commit()

    def update_allusertable(self, user_id, item, val):
        self.cursor.execute(
            "UPDATE AUT set {} = {} where ID = {}".format(item, val, user_id))
        self.conn.commit()

    def query_allusertable(self, user_id):
        data = self.cursor.execute(
            "SELECT USERNAME, PASSWD, LOGIN_STATUS from AUT where ID = {}".format(user_id))
        for row in data:
            return {"USERNAME": row[0], "PASSWD": row[1], "LOGIN_STATUS": row[2]}

    # ========== Message Table ==========

    def create_msgtable(self, user_id):
        table_name = "MSG" + str(user_id)
        self.cursor.execute(
            """
                CREATE TABLE {}
                (
                    SENDER_ID INT,
                    TIME TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    MSG TEXT NOT NULL
                )
            """.format(table_name)
        )
        self.conn.commit()

    def insert_msgtable(self, user_id, sender_id, msg):
        table_name = "MSG" + str(user_id)
        self.cursor.execute(
            """
                INSERT INTO {} (SENDER_ID, MSG)
                VALUES ({}, "{}")
            """.format(table_name, sender_id, msg)
        )
        self.conn.commit()

    def query_msgtable(self, user_id):
        table_name = "MSG" + str(user_id)

        data_list = []
        data = self.cursor.execute(
            "SELECT SENDER_ID, TIME, MSG from {}".format(table_name))
        for row in data:
            data_list.append(
                {"SENDER_ID": row[0], "TIME": row[1], "MSG": row[2]}
            )
        return data_list

    def erase_msgtable(self, user_id):
        table_name = "MSG" + str(user_id)
        self.cursor.execute("DELETE from {}".format(table_name))
        self.conn.commit()

    # ========== Friend List Table ==========

    def create_friendlisttable(self, user_id):
        table_name = "FL" + str(user_id)

        self.cursor.execute(
            """
                CREATE TABLE {}
                (
                    FRI_ID INT PRIMARY KEY NOT NULL
                )
            """.format(table_name)
        )
        self.conn.commit()

    def insert_friendlisttable(self, user_id, friend_id):
        table_name = "FL" + str(user_id)
        self.cursor.execute(
            """
                INSERT INTO {}  (FRI_ID)
                VALUES ({})
            """.format(table_name, friend_id)
        )
        self.conn.commit()

    def query_friendlisttable(self, user_id):
        table_name = "FL" + str(user_id)
        data_list = []
        data = self.cursor.execute("SELECT FRI_ID from {}".format(table_name))
        for row in data:
            data_list.append(row[0])
        return data_list

    def delete_friendlisttable(self, user_id, friend_id):
        table_name = "FL" + str(user_id)
        self.cursor.execute(
            "DELETE from {} where FRI_ID = {}".format(table_name, friend_id))
        self.conn.commit()

    # ========== Friend Request Table ==========

    def create_friendrequesttable(self, user_id):
        table_name = "FR" + str(user_id)
        self.cursor.execute(
            """
                CREATE TABLE {}
                (
                    FRI_ID INT PRIMARY KEY NOT NULL,
                    REQ_NOTE TEXT
                )
            """.format(table_name)
        )
        self.conn.commit()

    def insert_friendrequesttable(self, user_id, friend_id, req_note):
        table_name = "FR" + str(friend_id)
        self.cursor.execute(
            """
                INSERT INTO {} (FRI_ID, REQ_NOTE)
                VALUES ({}, '{}')
            """.format(table_name, user_id, req_note)
        )
        self.conn.commit()

    def query_friendrequesttable(self, user_id):
        table_name = "FR" + str(user_id)
        data_list = []
        data = self.cursor.execute(
            "SELECT FRI_ID, REQ_NOTE from {}".format(table_name))
        for row in data:
            data_list.append({"FRI_ID": row[0], "REQ_NOTE": row[1]})
        return data_list

    def delete_friendrequesttable(self, user_id, friend_id):
        table_name = "FR" + str(user_id)
        self.cursor.execute(
            "DELETE from {} where FRI_ID = {}".format(table_name, friend_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

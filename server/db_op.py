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


class dbOp:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # ========== ALL User Table ==========

    def create_allusertable(self):
        try:
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
            return 1
        except:
            return 0

    def insert_allusertable(self, user_id, user_name, passwd, login_status):
        try:
            self.cursor.execute(
                """
                    INSERT INTO AUT (ID, USERNAME, PASSWD, LOGIN_STATUS) 
                    VALUES ({}, '{}', '{}', {})
                """.format(user_id, user_name, passwd, login_status)
            )
            self.conn.commit()
            return 1
        except:
            return 0


    def delete_allusertable(self, user_id):
        try:
            self.cursor.execute("DELETE from AUT where ID={}".format(user_id))
            self.conn.commit()
            return 1
        except:
            return 0

    def update_allusertable(self, user_id, item, val):
        try:
            self.cursor.execute("UPDATE AUT set {} = {} where ID = {}".format(item, val, user_id))
            self.conn.commit()
            return 1
        except:
            return 0

    def query_allusertable(self, user_id):
        try:
            data = self.cursor.execute("SELECT USERNAME, PASSWD, LOGIN_STATUS from AUT where ID = {}".format(user_id))
            for row in data:
                return {"USERNAME": row[0], "PASSWD": row[1], "LOGIN_STATUS": row[2]}
        
        except:
            return None

    # ========== Message Table ==========

    def create_msgtable(self, user_id):
        table_name = "MSG" + str(user_id)
        try:
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
            return 1
        except:
            return 0

    def insert_msgtable(self, user_id, sender_id, msg):
        table_name = "MSG" + str(user_id)
        try:
            self.cursor.execute(
                """
                    INSERT INTO {} (SENSER_ID, MSG)
                    VALUES ({}, '{}')
                """.format(table_name, sender_id, msg)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def query_msgtable(self, user_id):
        table_name = "MSG" + str(user_id)
        
        data_list = []
        try:
            data = self.cursor.execute("SELECT SENDER_ID, TIME, MSG from {}".format(table_name))
            for row in data:
                data_list.append(
                    {"SENDER_ID": row[0], "TIME": row[1], "MSG": row[2]}
                )
            return data
        except:
            return None


    def erase_msgtable(self, user_id):
        table_name = "MSG" + str(user_id)
        try:
            self.cursor.execute("DELETE from {}".format(table_name))
            self.conn.commit()
            return 1
        except:
            return 0

    # ========== Friend List Table ==========

    def create_friendlisttable(self, user_id):
        table_name = "FL" + str(user_id)

        try:
            self.cursor.execute(
                """
                    CREATE TABLE {}
                    (
                        FRI_ID INT PRIMARY KEY NOT NULL
                    )
                """.format(table_name)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def insert_friendlisttable(self, user_id, friend_id):
        table_name = "FL" + str(user_id)
        try:
            self.cursor.execute(
                """
                    INSERT INTO {}  (FRI_ID)
                    VALUES ({})
                """.format(table_name, friend_id)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def query_friendlisttable(self, user_id):
        table_name = "FL" + str(user_id)
        data_list = []
        try:
            data = self.cursor.execute("SELECT FRI_ID from {}".format(table_name))
            for row in data:
                data_list.append(row[0])
            return data_list
        except:
            return None

    def delete_friendlisttable(self, user_id, friend_id):
        table_name = "FL" + str(user_id)
        try:
            self.cursor.execute("DELETE from {} where FRI_ID = {}".format(user_id, friend_id))
            self.conn.commit()
            return 1
        except:
            return 0


    # ========== Friend Request Table ==========

    def create_friendrequesttable(self, user_id):
        table_name = "FR" + str(user_id)
        try:
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
            return 1
        except:
            return 0

    def insert_friendrequesttable(self, user_id, friend_id, req_note):
        table_name = "FR" + str(user_id)
        try:
            self.cursor.execute(
                """
                    INSERT INTO {} (FRI_ID, REQ_NOTE)
                    VALUES ({}, '{}')
                """.format(table_name, friend_id, req_note)
            )
            self.conn.commit()
            return 1
        except:
            return 0

    

    def delete_friendrequesttable(self, user_id, friend_id):
        table_name = "FR" + str(user_id)
        try:
            self.cursor.execute("DELETE from {} where FRI_ID = {}".format(user_id, friend_id))
            self.conn.commit()
            return 1
        except:
            return 0
# MSG
# FRIEND_LIST
# FRIEND_REQUEST

# DB Structure:
# == MSGWITH<sender_id> ==
#   SENDER_ID, TIME, MSG
# == FL ==
#   FRIEND_ID
# == FR ==
#   Friend_id, req_note

import sqlite3

class dbOp:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_msgtable(self):
        try:
            self.cursor.execute(
                """
                    CREATE TABLE MSG
                    (
                        FRIEND_ID INT NOT NULL,
                        IMSENDER BOOL NOT NULL,
                        TIME TimeStamp NOT NULL,
                        MSG TEXT NOT NULL
                    )
                """
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def insert_msgtable(self, friend_id, imsender, time, msg):
        """
            Insert a message into msgtable
        """

        try:
            self.cursor.execute(
                """
                    INSERT INTO MSG (FRIEND_ID, IMSENDER, TIME, MSG)
                    VALUES ({}, {}, '{}', '{}')
                """.format(friend_id, imsender, time, msg)
            )
            self.conn.commit()
            return 1
        except:
            return 0
        pass

    def delete_msgtable(self, friend_id):
        """
            Delete all messages sent by sender_id
        """
        try:
            self.cursor.execute("DELETE from MSG where FRIEND_ID = {}".format(friend_id))
            self.conn.commit()
            return 1
        except:
            return 0
        pass

    def query_msgtable(self):
        try:
            data = self.cursor.execute("SELECT FRIEND_ID, IMSENDER, TIME, MSG from MSG")
            msg_dict = {}
            for row in data:
                if row[0] in msg_dict:
                    msg_dict[row[0]].append([row[1], row[2], row[3]])
                else:
                    msg_dict.update({row[0]: [[row[1], row[2], row[3]]]})
            return msg_dict

        except Exception as e:
            print(e)
            return 0
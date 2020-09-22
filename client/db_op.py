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
                        SENDER_ID INT NOT NULL,
                        TIME TimeStamp NOT NULL,
                        MSG TEXT NOT NULL
                    )
                """
            )
            self.conn.commit()
            return 1
        except:
            return 0

    def insert_msgtable(self, sender_id, time, msg):
        """
            Insert a message into msgtable
        """

        try:
            self.cursor.execute(
                """
                    INSERT INTO MSG (SENDER_ID, TIME, MSG)
                    VALUES ({}, '{}', '{}')
                """.format(sender_id, time, msg)
            )
            self.conn.commit()
            return 1
        except:
            return 0
        pass

    def delete_msgtable(self, sender_id):
        """
            Delete all messages sent by sender_id
        """
        try:
            self.cursor.execute("DELETE from MSG where SENDER_ID = {}".format(sender_id))
            self.conn.commit()
            return 1
        except:
            return 0
        pass
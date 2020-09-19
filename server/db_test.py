from db_op import dbOp
from random import randint
from threading import Thread

def dbinsert(tno):
    db_op_ins = dbOp("test.db")
    while True:
        print(
            tno,
            db_op_ins.insert_allusertable(randint(0, 999999999), "HAMA", 12345678, 0)
        )

if __name__ == "__main__":
    t1 = Thread(target = dbinsert, args = (1,))
    t2 = Thread(target = dbinsert, args = (2,))
    t1.start()
    t2.start()
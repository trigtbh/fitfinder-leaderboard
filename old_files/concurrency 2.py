from listform import Leaderboard, User
import threading
import uuid


lb = Leaderboard()

for i in range(1000):
    lb.add(User(uuid.uuid4(), i))

lb.add(User("a", 0))

import time

def add_thread():
    lb.update("a", 10001)

def get_thread():
    # time.sleep(0.0001)
    # print(lb.placement("a"))
    print(lb.adjacent("a"))
    print(lb.top_ten())


threading.Thread(target=add_thread).start()
threading.Thread(target=get_thread).start()
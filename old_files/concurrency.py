from listform import Leaderboard, User
import threading
import random

hashes = set()

def operation(lb, ids):
    lb.update(random.choice(ids), random.randint(0, len(ids)))


ids = "abcdefghijklmnopqrstuvwxyz"

for i in range(len(ids)):
    print(i)
    random.seed(100)
    lb = Leaderboard()

    for i in range(len(ids)):
        id_ = ids[i]
        lb.add(User(id_, random.randint(0, len(ids))))

    temp = str(lb)

    for _ in range(1000):
        # operation(lb, ids)
        t = threading.Thread(target=operation, args=(lb, ids))
        t.start()
        # t.join()

    assert temp != str(lb)

    hashes.add(hash(str(lb)))

print(len(hashes))
import bisect
import uuid
import random

def countingSort(arr, exp1):

    n = len(arr)

    output = [0] * (n)

    count = [0] * (10)

    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]


def radixSort(arr):

    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        countingSort(arr, exp)
        exp *= 10








class User:
    def __init__(self, uuid, score):
        self.uuid = uuid
        self.score = score

    def __gt__(self, other):
        if not isinstance(other, User):
            raise Exception("uh oh")
        return self.score > other.score
    
    def __lt__(self, other):
        if not isinstance(other, User):
            raise Exception("uh oh")
        return self.score < other.score


    def __repr__(self):
        return f"User('{self.uuid}' // {self.score})"

    def __truediv__(self, other):
        return self.score / other

    def __floordiv__(self, other):
        return self.score // other

    
class Leaderboard:
    def __init__(self):
        self.board = []

        self.users = {}

        self.lock = 0


    def initialize(self, users):
        while self.lock != 0: pass
        self.lock = 1
        for u in users:
            self.users[u.uuid] = u

        self.board = users
        radixSort(self.board)
        self.lock = 0


    def add(self, obj, ignore_exists=False):
        if not isinstance(obj, User):
            raise Exception("uh oh")

        if obj.uuid in self.users and not ignore_exists:
            raise ValueError(f"User with id '{obj.uuid}' already exists")

        while self.lock != 0:
            pass

        self.lock = 1

        self.users[obj.uuid] = obj
        
        bisect.insort_left(self.board, obj)

        self.lock = 0


    def __str__(self):
        return '\n'.join([f'{user.uuid} {user.score}' for user in self.board[::-1]])
    
    def find_first_index(self, A, low, high, key):
        if A[low].score == key.score:
            return low
        if low == high:
            return -1
        mid = low + (high - low) // 2
        if A[mid].score >= key.score:
            return self.find_first_index(A, low, mid, key)
        return self.find_first_index(A, mid + 1, high, key)

    def index(self, user: str | User):
        if isinstance(user, str):
            user = self.users[user]
        if not isinstance(user, User):
            raise Exception("uh oh")
        
        x = self.placement(user)
        if x == -1:
            return -1
        
        return -(x - len(self.board))

    def get(self, user: str):
        return self.users[user]

    def placement(self, user: str | User):
        if isinstance(user, str):
            user = self.users[user]
        if not isinstance(user, User):
            raise Exception("uh oh")
        
        while self.lock != 0: 
            pass

        self.lock = -1
        
        first_index = self.find_first_index(self.board, 0, len(self.board) - 1, user)
        if first_index == -1:
            self.lock = 0
            return -1
        while first_index < len(self.board) and self.board[first_index].score == user.score:
            if self.board[first_index].uuid == user.uuid:
                self.lock = 0
                return len(self.board) - first_index
            first_index += 1
        self.lock = 0
        return -1

    def adjacent(self, user: str | User):
        if isinstance(user, str):
            user = self.users[user]

        index = self.index(user)

        if index == -1:
            raise ValueError(f"User with id '{user.uuid}' not found")

        if len(self.board) == 1:
            return None, None
        if index == 0:
            return None, self.board[index + 1]
        if index == len(self.board) - 1:
            return self.board[index - 1], None
        return self.board[index - 1], self.board[index + 1]


    def top_ten(self):
        return self.board[-10:][::-1]

    def update(self, user: str | User, new_score: int):
        if isinstance(user, str):
            user = self.users[user]

        index = self.index(user)
        if index == -1:
            raise ValueError(f"User with id '{user.uuid}' not found")
        

        del self.board[index]
        user.score = new_score
        self.add(user, ignore_exists=True)
        

if __name__ == "__main__":
    leaderboard = Leaderboard()

    temp = []

    maxrange = 1_000_000

    for i in range(maxrange):
        user = User(uuid.uuid4(), random.randint(0, maxrange))
        temp.append(user)

    print("initializing...")

    leaderboard.initialize(temp)
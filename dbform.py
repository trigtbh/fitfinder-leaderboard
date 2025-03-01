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

conn_uri = "host='localhost' dbname='fflb' user='viscord' password='viscord'"




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

conn_uri = "host='localhost' dbname='viscord' user='viscord' password='viscord'"
conn = psycopg2.connect(creation_uri)
# conn.set_session()
cursor = conn.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS leaderboard (
id TEXT PRIMARY KEY,
score INTEGER
)
"""
)



class Leaderboard:
    def __init__(self, wipe=False):
        if wipe:
            cursor.execute(f"""
                CREATE TABLE leaderboard (
                id TEXT PRIMARY KEY,
                score INTEGER
                )
                """
            )



    def initialize(self, users):
        while self.lock != 0: pass
        self.lock = 1
        for u in users:
            self.users[u.uuid] = u

        self.board = users
        radixSort(self.board)
        self.lock = 0


    def insert(self, obj: str, ignore_exists=False):
        cursor.execute('''INSERT INTO leaderboard (id, score) values (%s, 0)''', (obj,))


    def __str__(self):
        return "NotImplemented"
        return '\n'.join([f'{user.uuid} {user.score}' for user in self.board[::-1]])
    
    def get(self, user: str):
        query = "SELECT score FROM leaderboard WHERE id = %s;"
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        return result[0] if result else None

    def placement(self, user: str):
        query = f"""
        SELECT RANK() OVER (ORDER BY score DESC) AS rank
        FROM leaderboard
        WHERE id = %s;"""
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        return result[0] if result else None

    def adjacent(self, user: str):
        query = """
            WITH Ranked AS (
                SELECT id, score, RANK() OVER (ORDER BY score DESC) AS rank
                FROM leaderboard
            )
            SELECT 
                (SELECT id FROM Ranked WHERE rank = (SELECT rank FROM Ranked WHERE id = %s) - 1) AS previous_user,
                (SELECT id FROM Ranked WHERE rank = (SELECT rank FROM Ranked WHERE id = %s) + 1) AS next_user
            FROM Ranked
            WHERE id = %s;
        """
        cursor.execute(query, (user, user, user))
        result = cursor.fetchone()
        return result[0], result[1]



        


    def top_ten(self):
        query = "SELECT id FROM leaderboard ORDER BY score DESC LIMIT 10;"
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def update(self, user: str, new_score: int):
        query = "UPDATE leaderboard SET score = %s WHERE id = %s;"
        cursor.execute(query, (new_score, user))
        

if __name__ == "__main__":
    leaderboard = Leaderboard()

    temp = []

    maxrange = 1_000_000

    for i in range(maxrange):
        user = User(uuid.uuid4(), random.randint(0, maxrange))
        temp.append(user)

    print("initializing...")

    leaderboard.initialize(temp)
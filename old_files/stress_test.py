from locust import HttpUser, between, task
import uuid
import random

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    def on_start(self):

        id_ = str(uuid.uuid4())

        self.client.post("/register_bypass", json={
            "uuid": id_
        })

        self.uuid = id_
    
    @task
    def manual_update(self):
        self.client.post("/update", json={
            "uuid": self.uuid,
            "score": random.randint(0, 10000)
        })

    @task
    def manual_score(self):
        self.client.post("/score", json={
            "uuid": self.uuid
        })

    @task
    def manual_adjacent(self):
        self.client.post("/adjacent", json={
            "uuid": self.uuid
        })

    @task
    def manual_top_ten(self):
        self.client.get("/top_ten")
    
    @task
    def manual_increment(self):
        self.client.post("/increment", json={
            "uuid": self.uuid,
            "increment": random.randint(0, 100)
        })

    @task
    def manual_placement(self):
        self.client.post("/placement", json={
            "uuid": self.uuid
        })

if __name__ == "__main__":
    import os
    # base = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(base)
    os.system(f"locust -f \"{__file__}\"")
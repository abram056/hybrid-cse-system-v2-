from locust import HttpUser, task, between
import random
import json
import os


def load_json(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data


SAMPLE_TEXTS = load_json(
    os.path.join(os.path.dirname(__file__), "sample_texts.json")
)


class APIUSer(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def health_check(self):
        self.client.get("/health")

    @task(3)
    def classify_text(self):
        sample = random.choice(SAMPLE_TEXTS)
        self.client.post("/analyse/", json=sample)

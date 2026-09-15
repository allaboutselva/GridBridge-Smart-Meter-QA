import requests
from config.settings import settings

class APIClient:
    def __init__(self, base_url=settings.api_base_url, timeout=settings.request_timeout):
        self.base_url = base_url.rstrip("/"); self.timeout = timeout; self.session = requests.Session()

    def login(self, username=settings.api_username, password=settings.api_password):
        response = self.post("/api/session", json={"username": username, "password": password})
        response.raise_for_status()
        token = response.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    def get(self, endpoint, **kwargs): return self.session.get(f"{self.base_url}{endpoint}", timeout=self.timeout, **kwargs)
    def post(self, endpoint, **kwargs): return self.session.post(f"{self.base_url}{endpoint}", timeout=self.timeout, **kwargs)

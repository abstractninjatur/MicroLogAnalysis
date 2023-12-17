import json

import logging

from login import Login



logger = logging.getLogger("api_client")

class APIClient:
    def __init__(self, ts_address: str, username="fdse_microservice", password="111111"):
        self.base_address = ts_address
        self.login = Login(ts_address)
        self.authenticated = self.login.login(username, password)
        if not self.authenticated:
            raise Exception("Authentication Failed")
        self.session = self.login.session

    def make_api_call(self, endpoint: str, method: str = "GET", params=None, data=None):
        if not self.authenticated:
            raise Exception("Not Authenticated")

        url = f"{self.base_address}/api/v1/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        print("URL : " + url + " Body : " + json.dumps(data))
        if method.upper() == "GET":
            response = self.session.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = self.session.post(url, json=data, params=params, headers=headers)
        elif method.upper() == "PUT":
            response = self.session.put(url, json=data, params=params, headers=headers)
        elif method.upper() == "DELETE":
            response = self.session.delete(url, json=data, params=params, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")


        if response.status_code in [200, 201, 204]:
            if response.json().get("data") is None:
                logger.warning(
                    f"query {url} failed, response data is {response.text}")
                return {}

            return response.json().get("data")
        print(response.json())
        # else:
        #     logging.error(f"API call failed: {response.status_code} {response.text}")
        #     return response.raise_for_status()

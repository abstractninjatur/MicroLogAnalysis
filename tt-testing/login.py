import requests
import logging


class Login:
    def __init__(self, ts_address: str) -> None:
        self.address = ts_address
        self.uid = ""
        self.token = ""
        self.session = requests.Session()
        self._initialize_session_headers()

    def _initialize_session_headers(self):
        self.session.headers.update({
            'Proxy-Connection': 'keep-alive',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        })

    def login(self, username="fdse_microservice", password="111111") -> bool:
        """
        Perform login and establish session. Return the login result.
        """
        url = f"{self.address}/api/v1/users/login"
        headers = {
            'Origin': self.address,
            'Referer': f"{self.address}/client_login.html",
        }
        data = {
            "username": username,
            "password": password,
            "verificationCode": "1234"
        }

        # Perform verification code retrieval (if necessary)
        self._get_verification_code()

        response = self.session.post(url=url, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            self._update_session_token(response)
            logging.info(f"Login successful, uid: {self.uid}")
            return True
        else:
            logging.error("Login failed")
            return False

    def _get_verification_code(self):
        verify_url = self.address + '/api/v1/verifycode/generate'
        self.session.get(url=verify_url)

    def _update_session_token(self, response):
        data = response.json().get("data")
        self.uid = data.get("userId")
        self.token = data.get("token")
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

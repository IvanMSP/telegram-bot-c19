import requests
import json


class Bot:

    def __init__(self, token):
        self.token = token

    def start_bot(self):
        pass


class ConnectionAPI:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_response(self, param: str) -> dict:
        endpoint = self.base_url + param
        response = requests.request("GET", endpoint)
        data = json.loads(response.text)
        return data


class Message:
    def __init__(self, type_message: int):
        self.type_message = type_message
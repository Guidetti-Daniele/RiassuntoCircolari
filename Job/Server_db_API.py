import requests
import traceback


class ServerDbAPI:

    def __init__(self, url, key):
        self.base_url = url
        self.key = key

    def get_missing_values(self, hashes):
        data = {
            'key': self.key,
            'hashes': hashes
        }

        try:
            response = requests.get(self.base_url + '/get_missing_values', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return []
        except Exception as ex:
            traceback.print_exc()
            return []

        return response.json()['data']

    def add_circ(self, *row_data):
        data = {
            'key': self.key,
            'data': list(row_data)
        }

        try:
            response = requests.put(self.base_url + '/add_circ', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return
        except Exception as ex:
            traceback.print_exc()
            return

    def add_comm(self, *row_data):
        data = {
            'key': self.key,
            'data': list(row_data)
        }

        try:
            response = requests.put(self.base_url + '/add_comm', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return
        except Exception as ex:
            traceback.print_exc()
            return

    def get_circ_hashes(self):
        data = {
            'key': self.key
        }

        try:
            response = requests.get(self.base_url + '/get_circ_hashes', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return []
        except Exception as ex:
            traceback.print_exc()
            return []

        return response.json()['data']

    def get_comm_hashes(self):
        data = {
            'key': self.key
        }

        try:
            response = requests.get(self.base_url + '/get_comm_hashes', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return []
        except Exception as ex:
            traceback.print_exc()
            return []

        return response.json()['data']

    def delete_circ(self, hash_):
        data = {
            'key': self.key,
            'hash': hash_
        }

        try:
            response = requests.delete(self.base_url + '/delete_circ', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return
        except Exception as ex:
            traceback.print_exc()
            return

    def delete_comm(self, hash_):
        data = {
            'key': self.key,
            'hash': hash_
        }

        try:
            response = requests.delete(self.base_url + '/delete_comm', json=data)
            if response.status_code != 200:
                print(f"request status code {response.status_code}\n{response.text}")
                return
        except Exception as ex:
            traceback.print_exc()
            return

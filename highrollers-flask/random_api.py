import requests
import json


class RandomAPI:
    def __init__(self):
        self.request_id = 0
        self.API_KEY = "14816d31-68c4-4e4b-bdd9-fae346054795"
        self.endpoint = "https://api.random.org/json-rpc/2/invoke"
    
    def send_request(self, method:str, params:dict) -> dict:

        all_params = {
            "apiKey": self.API_KEY,
        }
        all_params.update(params)
        json_args = {
            'jsonrpc': '2.0',
            'method': method,
            'params': all_params,
            'id': self.request_id,
        }
        self.request_id+=1
        headers = {'content-type': 'application/json'}
        response = requests.post(self.endpoint, data=json.dumps(json_args), headers=headers)
        response = response.json()
        if "error" in response:
            raise Exception(response["error"]['message'])
        return response["result"]

    def random_integer(self, min:int, max:int, count:int, replacement=True) -> list[int]:
        """Returns a list of random integers in the range [min, max] inclusive.
        :param int min: Lower boundary of the range
        :param int max: Upper boundary of the range
        :param int count: Number of integers to generate
        :param bool replacement: Whether the integers can be repeated
        :return: List of random integers"""

        response = self.send_request('generateIntegers', {'n': count, 'min': min, 'max': max, 'replacement': replacement})
        return response['random']['data']

    def random_decimal(self, min:float, max:float, count:int, decimal_places=8) -> list[float]:
        """Returns a list of random decimal numbers in the range [min, max).
        :param float min: Lower boundary of the range
        :param float max: Upper boundary of the range
        :param int count: Number of numbers to generate
        :param int decimal_places: Number of decimal places
        :return: List of random decimal numbers"""

        response = self.send_request('generateDecimalFractions', {'n': count, 'decimalPlaces': decimal_places})
        value = response['random']['data']
        value = [min + (max - min) * x for x in value]
        return value
    

if __name__ == "__main__":
    random_api = RandomAPI()
    print(random_api.random_decimal(1, 10, 5))
    print(random_api.random_integer(1, 10, 5))
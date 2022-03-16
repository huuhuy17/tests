import json


def connect_data(link):
    with open(link) as fin:
        data = fin.read()
        data_test = json.loads(data)
    return data_test

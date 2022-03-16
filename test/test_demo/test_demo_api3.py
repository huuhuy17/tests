from common.CONSTANT import POST, HEADERS
from common.connect_data import connect_data
from module.APIData import APIData
from module.TestExcute import TestExcute

# Thông tin api

SERVER = "http://10.2.22.100:8899"
RIGHT_URL = SERVER + "/v1/users/login"
RIGHT_METHOD = POST
DEMO_DATA = "login_data"
EXPECTED_TIME_REQUEST = 300  # ms

account_data = connect_data("../../data_test/test_demo.json")
headers_data = connect_data("../../config/headers.json")

data = account_data[DEMO_DATA]
headers = headers_data[HEADERS]


def test():
    api = APIData(DEMO_DATA, RIGHT_URL, RIGHT_METHOD, headers, data, EXPECTED_TIME_REQUEST)
    api.set_url()
    test_excute = TestExcute(api)
    test_excute.run()

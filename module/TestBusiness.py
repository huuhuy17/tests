import json
from abc import ABC
from datetime import datetime

import requests

from common.CONSTANT import GET, PUT, DELETE, POST, PATCH, HEADERS, DATA, WRONG_PARAMS, CODE, INJECTION_DATA, SUCCESS, \
    TOKEN, RESULT, USER_ID, WRONG_HEADERS, DEVICE_ID, HOME_ID, MEMBER_ID
from common.connect_data import connect_data
from module.APIData import APIData

headers_data = connect_data("../../config/headers.json")
headers = headers_data[HEADERS]
wrong_headers = headers_data[WRONG_HEADERS]


class TestBusiness(APIData, ABC):
    def __init__(self):
        super().__init__()

    def getName(self):
        return str(self.name)

    def setName(self, name):
        self.name = name

    def getUrl(self):
        return str(self.url)

    def setUrl(self, url):
        self.url = url
        if self.url.find(DEVICE_ID) != -1:
            device_id = str(self.data[DEVICE_ID])
            if device_id:
                self.url.replace('<device_id>', device_id)

        if self.url.find(HOME_ID) != -1:
            home_id = str(self.data[HOME_ID])
            if home_id:
                self.url.replace('<home_id>', home_id)

        if self.url.find(MEMBER_ID) != -1:
            member_id = str(self.data[MEMBER_ID])
            if member_id:
                self.url.replace('<member_id>', member_id)

        if self.url.find(USER_ID) != -1:
            user_id = str(self.data[USER_ID])
            if user_id:
                self.url.replace('<user_id>', user_id)

    def getMethod(self):
        return str(self.method)

    def setMethod(self, method):
        self.method = method

    def getHeaders(self):
        return self.headers

    def setHeaders(self, headers):
        self.headers = headers

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getExpectedTime(self):
        return self.expected_time

    def setExpectedTime(self, time):
        self.expected_time = time

    def test_method_not_allow(self):
        """
         Test phương thức sai
        """
        METHODS = {GET, PUT, PATCH, DELETE, POST}
        METHOD_ALLOWED = {self.getMethod()}
        # Phương thức không được phép
        METHODS_NOT_ALLOWED = METHODS - METHOD_ALLOWED
        for method in METHODS_NOT_ALLOWED:
            for item in self.getData():
                header = item[HEADERS]
                data = item[DATA]
                result = requests.request(method=method, url=self.getUrl(), headers=header, data=data)
                assert result.status_code == 405

    def test_url_wrong(self):
        """
        Test url sai
        """
        body = self.getData()[0][DATA]
        # Url sai
        wrong_url = self.getUrl() + "ss/abc123"
        result = requests.request(method=self.getMethod(), url=wrong_url, headers=self.getHeaders(), data=body)
        assert result.status_code == 404

    def test_param(self):
        """
        Test các trường hợp tham số sai
        """
        # Param sai định dạng
        # Param rỗng
        wrong_params = self.getData()[0].get(WRONG_PARAMS)
        for body in wrong_params:
            result = requests.request(method=self.getMethod(), url=self.getUrl(), headers=self.getHeaders(), data=body)
            assert result.status_code == 200
            assert result.json().get(CODE) == str(400)

    def test_authorization(self):
        """
        Test các truờng hợp headers sai
        """
        # Token rỗng
        # Token sai
        # Token hết hạn
        # Token sai phân quyền
        body = self.getData()[0][DATA]
        for header in wrong_headers:
            result = requests.request(method=self.getMethod(), url=self.getUrl(), headers=header, data=body)
            assert result.status_code == 200

    def test_sql_injection(self):
        """
        Test các trường hợp lỗi bảo mật SQL Injection
        """
        injection_data = self.getData()[0][INJECTION_DATA]
        for param in injection_data:
            body = json.dumps(param)
            result = requests.request(method=self.getMethod(), url=self.getUrl(), headers=self.getHeaders(), data=body)
            assert result.json().get(CODE) == str(403)

    def test_success_case(self):
        """
        Trường hợp thành công, test định dạng json, thời gian request, code success
        """
        time_start = datetime.now()
        result = requests.request(method=self.getMethod(), url=self.getUrl(), headers=self.getHeaders(),
                                  data=self.getData()[0][DATA])
        time_end = datetime.now()
        # HuyNH: Thời gian phản hồi
        delta = time_end - time_start
        # HuyNH: http succes
        assert result.status_code == 200
        # HuyNH: code success
        assert not result.json().get(SUCCESS)
        # HuyNH: Check type json
        assert type(result.json()) == dict
        # HuyNH: Check time request
        assert delta.microseconds / 1000 <= self.getExpectedTime()
        if result.json().get(SUCCESS):
            self.getHeaders()[TOKEN] = result.json().get(RESULT).get(TOKEN)
            self.getHeaders()[USER_ID] = result.json().get(RESULT).get(USER_ID)

    def run_all_test(self):
        self.test_method_not_allow()
        self.test_url_wrong()
        self.test_param()
        self.test_param()
        self.test_authorization()
        self.test_sql_injection()
        self.test_success_case()



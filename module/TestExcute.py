from common.CONSTANT import GET
from module import TestBusiness


class TestExcute():
    def __init__(self, api: TestBusiness):
        self.api = api

    def run(self):
        self.api.test_method_not_allow()
        self.api.test_url_wrong()
        self.api.test_authorization()
        # Nếu phương thức là GET thì không test param
        if self.api.getMethod() != GET:
            self.api.test_param()
            self.api.test_sql_injection()
        self.api.test_success_case()

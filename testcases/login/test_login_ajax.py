import allure
from playwright.sync_api import expect

from common.log_utils import logs


# @allure.feature("Ajax异步请求与响应断言的两个测试用例")
class TestLogin:
    """Ajax异步请求与响应断言的两个测试用例"""

    def test_01_login_success(self, login_page):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16位正确密码
        """
        login_page.navigate(url="/auth")
        login_page.input_email("admin@163.com")
        login_page.input_password("AaAa123456")
        with login_page.page.expect_request("**/api/v1/auths/signin") as req:
            login_page.click_login_button()

        assert req.value.method == "POST"
        assert "application/json" in req.value.header_value("content-type")
        assert req.value.post_data_json == {"email": "admin@163.com", "password": "AaAa123456"}
        logs.info("登录失败-请输入密码")

    def test_02_login_success(self, login_page):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16大写字母+小写字母+特殊符号
        """
        login_page.navigate(url="/auth")
        login_page.input_email("test1@163.com")
        login_page.input_password("AaAaAaAa!!")
        with login_page.page.expect_response("**/api/v1/auths/signin") as res:
            login_page.click_login_button()
        assert res.value.status == 200

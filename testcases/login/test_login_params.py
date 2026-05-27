import pytest
from playwright.sync_api import expect

from common.get_json_data import get_json_data
from common.log_utils import logs


class TestLogin:
    """
    登录测试用例的参数化
    """

    @pytest.mark.parametrize("email,password,attribute_name,attribute_value,title",
                             get_json_data("data/login_success_data.json"))
    def test_01_login_success(self, login_page, email, password, attribute_name, attribute_value, title):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16位正确密码
        """
        login_page.login(email, password)
        # 断言登陆后的page的页面标题
        expect(login_page.login_input_text).to_have_attribute(attribute_name, attribute_value, timeout=10000)
        expect(login_page.page).to_have_title(title)
        logs.info("登录成功" + title)

    @pytest.mark.parametrize("email,password,email_or_password_error,locator_method",
                             get_json_data("data/login_fail_data.json"))
    def test_02_login_fail(self, login_page, email, password, email_or_password_error, locator_method):
        """
        邮箱为空
        """
        login_page.login(email, password)
        # 断言
        error_locator = getattr(login_page, locator_method)
        expect(error_locator).to_be_visible()
        expect(error_locator).to_contain_text(email_or_password_error)
        logs.info("登录失败" + email_or_password_error)

    def test_03_login_fail(self, login_page):
        """
        邮箱不存在
        """
        login_page.login("admin123@163.com", "Aa123456")
        # 断言
        expect(login_page.page.get_by_text(
            "The email or password provided is incorrect. Please check for typos and try logging in again")).to_be_visible()

        logs.info("登录失败-邮箱不存在")

    def test_04_login_fail(self, login_page):
        """
        密码不存在
        """
        login_page.login("admin@163.com", "Aa1234561")
        # 断言
        expect(login_page.page.get_by_text(
            "The email or password provided is incorrect. Please check for typos and try logging in again")).to_be_visible()
        logs.info("登录失败-密码不存在")

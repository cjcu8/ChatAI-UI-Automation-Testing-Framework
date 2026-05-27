from playwright.sync_api import expect

from common.log_utils import logs
from pages.add_users_page import AddUsersPage


class TestAddUsers:
    def test_01_add_users_success(self, logged_in_page):
        adduser = AddUsersPage(logged_in_page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(adduser.chat_input).to_be_visible(timeout=100000)
        adduser.add_users_process("test8", "test8@163.com", "AaAa123456")
        expect(logged_in_page.get_by_text("test8", exact=True)).to_contain_text("test8")
        logged_in_page.screenshot(path="./test_results/add_users/add_user_success.png")
        logs.info(f"添加用户成功")

    def test_02_add_users_fail(self, logged_in_page):
        adduser = AddUsersPage(logged_in_page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(adduser.chat_input).to_be_visible(timeout=100000)
        adduser.add_users_process("test1", "test1@163.com", "AaAa123456")
        expect(adduser.email_repeat).to_contain_text("This email is already registered")
        logged_in_page.screenshot(path="./test_results/add_users/add_user_fail_01.png")
        logs.info(f"添加用户失败-This email is already registered")

    def test_03_add_users_fail(self, logged_in_page):
        adduser = AddUsersPage(logged_in_page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(adduser.chat_input).to_be_visible(timeout=100000)
        adduser.add_users_process("test6", "test5@163", "AaAa123456")
        expect(adduser.email_format_error).to_contain_text("The email format you entered is invalid.")
        logged_in_page.screenshot(path="./test_results/add_users/add_user_fail_02.png")
        logs.info(f"添加用户失败-The email format you entered is invalid.")


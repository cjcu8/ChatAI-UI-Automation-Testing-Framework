from playwright.sync_api import expect

from common.log_utils import logs
from pages.exit_login import ExitLogin


class TestExitLogin:
    """
    退出登录
    """

    def test_exit_login(self, logged_in_page):
        exitlogin = ExitLogin(logged_in_page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(exitlogin.chat_input).to_be_visible(timeout=100000)
        logs.info("登录成功")
        exitlogin.exit_login()
        expect(exitlogin.exit_success).to_be_visible(timeout=100000)
        logged_in_page.screenshot(path="./test_results/exit_login/exit_success.png")

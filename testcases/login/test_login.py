from playwright.sync_api import expect

from common.log_utils import logs


class TestLogin:
    """登录的10条测试用例"""

    def test_01_login_success(self, login_page):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16位正确密码
        """
        login_page.login("admin@163.com", "AaAa123456")
        # 断言登陆后的page的页面标题
        expect(login_page.login_input_text).to_have_attribute("data-placeholder", "有什么我能帮您的吗？", timeout=10000)
        expect(login_page.page).to_have_title("Open WebUI")
        login_page.page.screenshot(path="./test_results/login/login_success01.png")
        logs.info("登录成功-页面标题显示：Open WebUI-输入框信息显示：有什么我能帮您的吗？")

    def test_02_login_success(self, login_page):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16大写字母+小写字母+特殊符号
        """
        login_page.login("test1@163.com", "AaAaAaAa!!")
        expect(login_page.login_input_text).to_have_attribute("data-placeholder", "有什么我能帮您的吗？", timeout=10000)
        # 断言登陆后的page的页面标题
        expect(login_page.page).to_have_title("Open WebUI")
        login_page.page.screenshot(path="./test_results/login/login_success02.png")
        logs.info("登录成功-页面标题显示：Open WebUI-输入框信息显示：有什么我能帮您的吗？")

    def test_03_login_success(self, login_page):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16大写字母+数字+特殊符号
        """
        login_page.login("test2@163.com", "AA123456!!")
        expect(login_page.login_input_text).to_have_attribute("data-placeholder", "有什么我能帮您的吗？", timeout=10000)
        expect(login_page.page).to_have_title("Open WebUI")
        login_page.page.screenshot(path="./test_results/login/login_success03.png")
        logs.info("登录成功-页面标题显示：Open WebUI-输入框信息显示：有什么我能帮您的吗？")

    def test_04_login_success(self, login_page):
        """
        测试登录成功
        email:已注册邮箱
        密码：8-16大写字母+小写字母+数字+特殊符号
        """
        login_page.login("test3@163.com", "Aa123456!!")
        expect(login_page.login_input_text).to_have_attribute("data-placeholder", "有什么我能帮您的吗？", timeout=10000)
        # 断言登陆后的page的页面标题
        expect(login_page.page).to_have_title("Open WebUI")
        login_page.page.screenshot(path="./test_results/login/login_success04.png")
        logs.info("登录成功-页面标题显示：Open WebUI-输入框信息显示：有什么我能帮您的吗？")


    def test_05_login_fail(self, login_page):
        """
        注册失败，邮箱为空
        """
        login_page.login("", "Aa123456")
        # 断言
        expect(login_page.email_empty_error).to_be_visible()
        expect(login_page.email_empty_error).to_contain_text("请输入电子邮箱")
        login_page.page.screenshot(path="./test_results/login/login_fail01.png")
        logs.info("登录失败-请输入电子邮箱")

    def test_06_login_fail(self, login_page):
        """
        注册失败，邮箱格式不正确
        """
        login_page.login("admin@163", "Aa123456")
        # 断言
        expect(login_page.email_format_error).to_be_visible()
        expect(login_page.email_format_error).to_contain_text("请输入正确的电子邮箱格式")
        login_page.page.screenshot(path="./test_results/login/login_fail02.png")
        logs.info("登录失败-请输入正确的电子邮箱格式")

    def test_07_login_fail(self, login_page):
        """
        注册失败，邮箱不存在
        """
        login_page.login("admin123@163.com", "Aa123456")
        # 断言
        expect(login_page.page.get_by_text(
            "The email or password provided is incorrect. Please check for typos and try logging in again")).to_be_visible()
        login_page.page.screenshot(path="./test_results/login/login_fail03.png")
        logs.info("登录失败-邮箱不存在")

    def test_08_login_fail(self, login_page):
        """
        注册失败，密码不存在
        """
        login_page.login("admin@163.com", "Aa1234561")
        # 断言
        expect(login_page.page.get_by_text(
            "The email or password provided is incorrect. Please check for typos and try logging in again")).to_be_visible()
        login_page.page.screenshot(path="./test_results/login/login_fail04.png")
        logs.info("登录失败-密码不存在")

    def test_09_login_fail(self, login_page):
        """
        注册失败，密码为空
        """
        login_page.login("admin@163.com", "")
        # 断言
        expect(login_page.password_empty_error).to_be_visible()
        expect(login_page.password_empty_error).to_contain_text("请输入密码")
        login_page.page.screenshot(path="./test_results/login/login_fail05.png")
        logs.info("登录失败-请输入密码")

    def test_10_login_fail(self, login_page):
        """
        注册失败，密码格式错误
        """
        login_page.login("admin@163.com", "A1231AA23")
        # 断言
        expect(login_page.password_error).to_be_visible()
        expect(login_page.password_error).to_contain_text("密码至少包含大写字母、小写字母、数字、特殊符号中的3类")
        login_page.page.screenshot(path="./test_results/login/login_fail06.png")
        logs.info("登录失败-密码至少包含大写字母、小写字母、数字、特殊符号中的3类")



from playwright.sync_api import expect

from common.log_utils import logs


def handle1(route):
    route.fulfill(
        status=502,
        content_type="application/json",
        body='{"detail":"Bad Gateway"}'
    )

def handle2(route):
    route.fulfill(
        status=500,
        content_type="application/json",
        body='{"detail":"Internal Server Error"}'
    )


class TestMockLogin:
    """mock模拟服务器异常，测试登录接口异常"""

    def test_01_login_api_502(self,login_page):
        """
        测试登录接口异常
        场景：登录接口返回 502
        """
        page = login_page.page

        login_page.navigate("/auth")
        login_page.input_email("admin@163.com")
        login_page.input_password("AaAa123456")

        # 点击登录前注册拦截
        page.route("**/api/v1/auths/signin", handler=handle1)

        # 触发登录请求
        login_page.click_login_button()
        expect(page.get_by_text("Bad Gateway")).to_be_visible(timeout=5000)
        logs.info("登录成功-Bad Gateway")

    def test_02_login_api_502(self,login_page):
        """
        测试登录接口异常
        场景：登录接口返回 500
        """
        page = login_page.page

        login_page.navigate("/auth")
        login_page.input_email("admin@163.com")
        login_page.input_password("AaAa123456")

        # 点击登录前注册拦截
        page.route("**/api/v1/auths/signin", handler=handle2)

        # 触发登录请求
        login_page.click_login_button()
        expect(page.get_by_text("Internal Server Error")).to_be_visible(timeout=5000)
        logs.info("登录成功-Internal Server Error")

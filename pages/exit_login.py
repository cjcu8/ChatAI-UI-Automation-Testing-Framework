from playwright.sync_api import expect


class ExitLogin:

    def __init__(self, page):
        self.page = page
        # 定位输入框
        self.chat_input = page.locator("#chat-input > [data-placeholder='有什么我能帮您的吗？']")
        # 定位右上角头像
        self.avatar = page.get_by_role("navigation").locator("img")
        # 退出
        self.exit = page.get_by_text("登出")

        # 断言退出登录成功
        self.exit_success = page.get_by_text("登录 Open WebUI", exact=True)

    def exit_login(self):
        self.avatar.click()
        expect(self.avatar).to_be_visible(timeout=10000)
        self.exit.click()
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        # 初始化登录页面对象
        self.page = page
        # 定位元素
        # 定位邮箱输入框
        self.email_input = page.locator("#email")
        # 定位密码输入框
        self.password_input = page.get_by_placeholder("输入您的密码")
        # 登录按钮
        self.login_button = page.get_by_text("登录", exact=True)
        # 断言元素的抓取
        # 登陆成功定位输入框文本-get_by_role("paragraph")
        self.login_input_text = page.locator("#chat-input > [data-placeholder='有什么我能帮您的吗？']")
        # 邮箱为空
        self.email_empty_error = page.get_by_text("请输入电子邮箱")
        # 邮箱格式错误
        self.email_format_error = page.get_by_text("请输入正确的电子邮箱格式")
        # 密码为空
        self.password_empty_error = page.get_by_text("请输入密码")
        # 密码类型错误
        self.password_error = page.get_by_text("密码至少包含大写字母、小写字母、数字、特殊符号中的3类")
        # 密码长度错误
        self.password_length_error = page.get_by_text("密码长度必须为8~16位")

    def navigate(self,url):
        """
        导航到登录页面
        """
        self.page.goto(url)

    def input_email(self, email):
        """
        输入邮箱
        :param email: 邮箱号
        """
        self.email_input.fill(email)

    def input_password(self, password):
        """
        输入密码
        :param password: 密码
        """
        self.password_input.fill(password)

    def click_login_button(self):
        """
        点击登录按钮
        """
        self.login_button.click()

    # 登录业务
    def login(self,email, password,url="/auth"):
        self.navigate(url)
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.login("admin@163.com", "AaAa123456")
        page.pause()
        print(login_page.login_input_text.count())
        page.close()

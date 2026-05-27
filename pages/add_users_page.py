
# 后台添加用户page
class AddUsersPage:

    def __init__(self, page):
        # 定位输入框
        self.chat_input = page.locator("#chat-input > [data-placeholder='有什么我能帮您的吗？']")
        # 定位右上角头像
        self.avatar = page.get_by_role("navigation").locator("img")
        # 定位管理员面板
        self.admin_panel = page.get_by_text("管理员面板")
        # 添加用户
        self.add_users = page.get_by_role("button").nth(3)
        # 定位到角色列表,选择“用户”
        self.role_list = page.get_by_placeholder("输入您的用户组")
        # 定位输入用户名输入框
        self.username_input = page.get_by_placeholder("输入您的名称")
        # 定位输入电子邮箱
        self.email_input = page.get_by_placeholder("输入您的电子邮箱")
        # 输入密码
        self.password_input = page.get_by_placeholder("输入您的密码")
        # 保存
        self.save_button = page.get_by_text("保存")
        # 电子邮箱重复
        self.email_repeat = page.get_by_text("Uh-oh! This email is already registered")
        # 电子邮箱格式错误
        self.email_format_error = page.get_by_text("The email format you entered is invalid.")



    # 点击右上角头像
    def click_avatar(self):
        self.avatar.click()

    # 点击管理员面板
    def click_admin_panel(self):
        self.admin_panel.click()

    # 点击添加用户
    def click_add_users(self):
        self.add_users.click()

    # 选择用户角色
    def select_role(self):
        self.role_list.select_option("用户")

    # 输入用户名
    def input_username(self, username):
        self.username_input.fill(username)

    # 输入邮箱
    def input_email(self, email):
        self.email_input.fill(email)

    # 输入密码
    def input_password(self, password):
        self.password_input.fill(password)

    # 点击保存
    def click_save(self):
        self.save_button.click()

    # 添加用户流程
    def add_users_process(self, username, email, password):
        self.click_avatar()
        self.click_admin_panel()
        self.click_add_users()
        self.select_role()
        self.input_username(username)
        self.input_email(email)
        self.input_password(password)
        self.click_save()
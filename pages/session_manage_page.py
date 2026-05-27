from playwright.sync_api import expect


class SessionManagePage:
    def __init__(self, page):
        self.page = page
        # 定位展开侧边栏
        self.expand_sidebar = page.get_by_role("button", name="展开侧边栏", exact=True)
        # 对话列表
        self.session_items = self.page.locator("#sidebar-chat-group")

        # 删除
        self.delete_button = page.get_by_role("button", name="删除")
        # 重命名
        self.rename_button = page.get_by_role("button", name="重命名")
        # 确认删除
        self.confirm_delete_button = page.get_by_role("button", name="确认")

        self.rename_session_input = page.locator("input[id^='chat-title-input']")
        # 定位输入框
        self.chat_input = page.locator("#chat-input > [data-placeholder='有什么我能帮您的吗？']")

    # 重命名对话
    def rename_session(self, session_name, session_name_new):
        self.expand_sidebar.click()
        expect(self.session_items.first).to_be_visible(timeout=10000)
        session_items_count_before = self.session_items.count()
        session_item = self.session_items.filter(has_text=session_name).first
        session_item.hover()
        expect(session_item.locator("button")).to_be_visible(timeout=10000)
        session_item.locator("button").click()
        self.rename_button.click()
        self.rename_session_input.fill(session_name_new)
        self.rename_session_input.press("Enter")
        self.chat_input.click()
        # 断言 1：重命名后会话数量不变
        expect(self.session_items).to_have_count(session_items_count_before, timeout=10000)
        # 断言 2：新名称出现
        new_session_item = self.session_items.filter(has_text=session_name_new).first
        expect(new_session_item).to_be_visible(timeout=10000)
        # 断言 3：新名称确实在目标会话中
        expect(new_session_item).to_contain_text(session_name_new, timeout=10000)
        self.page.screenshot(path="./test_results/session_manage/session_rename_success.png")

    # 对话删除
    def delete_session(self, session_name):
        self.expand_sidebar.click()
        expect(self.session_items.first).to_be_visible(timeout=10000)
        session_items_count_before = self.session_items.count()
        session_item = self.session_items.filter(has_text=session_name).first
        session_item.hover()
        print(session_item.count())
        expect(session_item.locator("button")).to_be_visible(timeout=10000)
        session_item.locator("button").click()
        self.delete_button.click()
        self.page.screenshot(path="./test_results/session_manage/session_delete_success.png")
        self.confirm_delete_button.click()
        # 关键：等待会话数量减少 1
        expect(self.session_items).to_have_count(session_items_count_before, timeout=100000)
        # 再获取删除后数量
        session_items_count_after = self.session_items.count()
        print("删除后会话数量：", session_items_count_after)
        print("删除前会话数量：", session_items_count_before)

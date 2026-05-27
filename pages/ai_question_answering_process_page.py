from playwright.sync_api import Page
from playwright.sync_api import expect


class AIQuestionAnsweringProcessPage:

    def __init__(self, page: Page):
        # 页面对象
        self.page = page
        # 模型选择
        self.model_select = page.locator("button[aria-haspopup='listbox']")
        # 选择qwen大模型
        # self.qwen_model = page.get_by_text("qwen3.5:2b")
        self.qwen_model = page.get_by_role("option", name='选择模型 “deepseek-r1:1.5b”')
        # 设置为默认模型
        self.set_default_model = page.get_by_text("设为默认")
        # 模型更新断言
        self.model_update_text = page.get_by_text("默认模型已更新")
        # 定位输入框
        self.chat_input = page.locator("#chat-input > [data-placeholder='有什么我能帮您的吗？']")
        # 定位发送按钮
        self.send_button = page.locator("#send-message-button")
        # 定位语音按钮
        self.voice_button = page.locator("button[aria-label='语音模式']")
        # 定位停止按钮
        self.stop_button = page.locator("#message-input-container .bg-white")
        # 获取所有文本信息
        self.message_items = page.locator("div[role='listitem']")

    # 模型选择
    def modelselect(self):
        self.model_select.click()

    # 选择qwen大模型
    def select_qwen_model(self):
        self.qwen_model.click()

    # 设置为默认模型
    def set_qwen_default_model(self):
        self.set_default_model.click()

    # 聊天框输入文本
    def input_text(self, text):
        self.chat_input.fill(text)

    # 点击发送
    def click_send(self):
        self.send_button.wait_for(state="visible", timeout=5000)
        self.send_button.click()

    def UserChatProcess(self, text):
        expect(self.chat_input).to_be_visible(timeout=1000000)
        self.modelselect()
        self.select_qwen_model()
        self.input_text(text)
        self.click_send()

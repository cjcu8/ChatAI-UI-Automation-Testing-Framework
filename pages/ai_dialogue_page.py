class AIDialoguePage:

    def __init__(self, page):
        self.page = page
        # 定位新建对话
        self.new_dialogue = page.get_by_text("新对话")
        # 模型选择
        self.model_select = page.locator("button[aria-haspopup='listbox']")
        # 选择qwen大模型
        self.qwen_model = page.get_by_text("qwen3.5:2b")
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

        # 上传文件对话
        self.upload_file = page.locator("#input-menu-button")
        # 上传文件按钮
        self.upload_file_button = page.get_by_text("上传文件")

        # 点击复制按钮
        self.copy_button = self.message_items.locator("[aria-label='复制']")

    # 新建对话
    def new_chat(self):
        self.new_dialogue.click()

    # 模型选择
    def modelselect(self):
        self.model_select.click()

    # 选择qwen大模型
    def select_qwen_model(self):
        self.qwen_model.click()

    # 定位输入框
    def input_text(self, text):
        self.chat_input.fill(text)

    # 点击发送
    def click_send(self):
        self.send_button.click()

    # 点击上传文件
    def click_upload_file(self,file_path):
        self.upload_file.click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_text("上传文件").click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)

    # # 定位对应的回复文本悬停，然后复制
    # def copy_text(self):
    #     self.message_items.hover()
    #     self.copy_button.click()
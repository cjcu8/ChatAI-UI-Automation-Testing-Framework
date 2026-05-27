
class UploadFileOperation:

    def __init__(self,page):
        self.page = page
        # 定位输入框
        self.chat_input = page.locator("#chat-input > [data-placeholder='有什么我能帮您的吗？']")
        # 定位新建对话
        self.new_dialogue = page.get_by_text("新对话")
        # 上传文件对话
        self.upload_file = page.locator("#input-menu-button")
        # 上传文件按钮
        self.upload_file_button = page.get_by_text("上传文件")
        # 断言上传的图片
        self.uploaded_image = page.locator("#message-input-container img[data-cy='image']").last

    # 点击上传文件
    def click_upload_file(self, file_path):
        self.upload_file.click()
        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_text("上传文件").click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)
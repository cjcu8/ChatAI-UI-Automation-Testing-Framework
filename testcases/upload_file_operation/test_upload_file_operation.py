import re

from playwright.sync_api import expect

from common.get_json_data import BASE_DIR
from common.log_utils import logs
from pages.upload_file_operation_page import UploadFileOperation


class TestUploadFileOperation:
    def test_01_upload_file_png(self, logged_in_page):
        page = logged_in_page
        up_file=UploadFileOperation(page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(up_file.chat_input).to_be_visible(timeout=100000)
        logs.info("首页加载成功")
        up_file.click_upload_file(BASE_DIR / "data" / "chatfile" / "狐狸.png")
        # 断言图片缩略图显示
        expect(up_file.uploaded_image).to_be_visible(timeout=30000)
        # 断言图片 src 是上传后的文件接口
        expect(up_file.uploaded_image).to_have_attribute(
            "src",
            re.compile(r"/api/v1/files/.+/content"),
            timeout=30000
        )
        # expect(AIDP.stop_button).to_have_count(2, timeout=10000)
        logs.info("png文件上传成功")
        page.screenshot(path=f"./test_results/upload_file/upload_file_png.png")

    def test_02_upload_file_jpg(self, logged_in_page):
        page = logged_in_page
        up_file=UploadFileOperation(page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(up_file.chat_input).to_be_visible(timeout=100000)
        logs.info("首页加载成功")
        up_file.click_upload_file(BASE_DIR / "data" / "chatfile" / "狐狸.jpg")
        # 断言图片缩略图显示
        expect(up_file.uploaded_image).to_be_visible(timeout=30000)
        # 断言图片 src 是上传后的文件接口
        expect(up_file.uploaded_image).to_have_attribute(
            "src",
            re.compile(r"/api/v1/files/.+/content"),
            timeout=30000
        )
        # expect(AIDP.stop_button).to_have_count(2, timeout=10000)
        logs.info("jpg文件上传成功")
        page.screenshot(path=f"./test_results/upload_file/upload_file_jpg.jpg")
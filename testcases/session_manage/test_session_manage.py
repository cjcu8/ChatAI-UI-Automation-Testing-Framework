from playwright.sync_api import expect

from common.log_utils import logs
from pages.session_manage_page import SessionManagePage


class TestSessionManage:

    def test_01_rename_session(self, logged_in_page):
        session_manage = SessionManagePage(logged_in_page)
        session_manage.rename_session("你是谁？", "deepseek")

        logs.info(f"会话添加成功-对话数量不变，deepseek-出现在对话列表中")

    # 根据对话框名字，模糊匹配删除对话框
    def test_02_delete_session(self, logged_in_page):
        session_manage = SessionManagePage(logged_in_page)
        session_manage.delete_session("deepseek")

        logs.info(f"会话删除成功-对话数量减一")

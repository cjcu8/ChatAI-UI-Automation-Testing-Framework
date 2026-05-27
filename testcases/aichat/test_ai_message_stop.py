import re

import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

from common.get_json_data import get_json_data
from common.log_utils import logs
from common.userchat_info_write import user_chat_info_write
from pages.ai_dialogue_page import AIDialoguePage


class TestMessageStop:
    """
    测试用户停止模型回复
    """

    def test_01_ai_dialogue_message_stop(self, logged_in_page):
        """
        模型终止回复
        """
        page = logged_in_page
        # 创建AI聊天对象
        AIDP = AIDialoguePage(page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(AIDP.chat_input).to_be_visible(timeout=100000)
        # 输入问题，提问大模型
        AIDP.input_text("只回复，'WEB UI自动化测试'，不要回答其他内容？")
        # 断言发送按钮显示，并记录日志
        expect(AIDP.send_button).to_be_visible(timeout=10000)
        logs.info("发送按钮显示")
        AIDP.click_send()
        expect(AIDP.stop_button).to_be_visible(timeout=10000)
        AIDP.stop_button.click()
        # 断言语音按钮显示（等待模型回复完成），记录日志
        expect(AIDP.voice_button).to_be_visible(timeout=1000000)
        logs.info("语音按钮显示")
        page.screenshot(path=f"./test_results/ai_dialogue_record/chat_message_stop.jpg")
        logs.info("回答停止")

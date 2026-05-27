import re

import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

from common.get_json_data import get_json_data
from common.log_utils import logs
from common.userchat_info_write import user_chat_info_write
from pages.ai_dialogue_page import AIDialoguePage


class TestMessageCopy:
    """复制模型生成的消息"""

    def test_01_ai_dialogue_message_copy(self, logged_in_page):
        """
        复制模型生成的消息的测试用例
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
        # 断言语音按钮通常会隐藏，记录日志
        expect(AIDP.voice_button).to_be_hidden(timeout=10000)
        logs.info("语音按钮隐藏")
        # 模型生成时，停止按钮应该出现，但不是必须得，因为停止按钮可能定位不到
        try:
            expect(AIDP.stop_button).to_be_visible(timeout=1000000)
            logs.info("停止按钮出现")
        except PlaywrightTimeoutError:
            logs.info("未捕获到停止按钮，可能模型回复较快或停止按钮定位不稳定")
        # 断言语音按钮显示（等待模型回复完成），记录日志
        expect(AIDP.voice_button).to_be_visible(timeout=1000000)
        logs.info("语音按钮显示")
        # 通过定位消息盒子，获取提问大模型和大模型回复的数量
        old_count = AIDP.message_items.count()
        # 定位提问大模型文本
        latest_message_question = AIDP.message_items.nth(old_count - 2)
        # 定位大模型回复文本
        latest_message_answer = AIDP.message_items.nth(old_count - 1)

        page.context.grant_permissions(
            ["clipboard-read", "clipboard-write"],
            origin="http://localhost:5173"
        )
        # 悬停模型回复文本，并点击复制
        latest_message_answer.hover()
        copy_button = latest_message_answer.locator("[aria-label='复制']").last
        expect(copy_button).to_be_visible(timeout=10000)
        copy_button.click()
        clipboard_text = page.evaluate("navigator.clipboard.readText()")
        assert "自动化测试" in clipboard_text
        assert clipboard_text.strip() != "", "剪贴板内容为空，复制失败"
        logs.info("复制成功，包含文本，以及剪切板不为空")
        # 获取提问大模型文本和模型回复文本
        question = latest_message_question.inner_text().strip()
        answer = latest_message_answer.inner_text().strip()
        # 断言模型回复不为空，记录日志，并截图
        expect(latest_message_answer).to_contain_text(re.compile(r"\S+"), timeout=30000)
        logs.info("模型回答不为空")

        page.screenshot(path=f"./test_results/ai_dialogue_record/chat_message_copy.jpg")
        user_chat_info_write(question, answer, r".\test_results\ai_dialogue_record\chat_message_copy.txt")


import re

import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

from common.get_json_data import get_json_data
from common.log_utils import logs
from common.userchat_info_write import user_chat_info_write
from pages.ai_dialogue_page import AIDialoguePage


class TestMessageRegenerate:
    """
    大模型回复消息后，重新生成
    """

    def test_01_ai_dialogue_message_regenerate(self, logged_in_page):
        """
        重新生成测试用例
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
        page.screenshot(path=f"./test_results/ai_dialogue_record/chat_message_regenerate1.jpg")
        logs.info("回答完毕等待重新生成")
        # 悬停模型回复文本，并点击复制
        latest_message_answer.hover()
        regenerate_menu_button = latest_message_answer.locator("[aria-label='重新生成']")
        expect(regenerate_menu_button).to_be_visible(timeout=10000)
        regenerate_menu_button.click()
        regenerate_button = page.get_by_text("重新生成", exact=True).locator("xpath=ancestor::button[1]")
        expect(regenerate_button).to_be_visible(timeout=10000)
        regenerate_button.click()
        try:
            expect(AIDP.stop_button).to_be_visible(timeout=1000000)
            logs.info("停止按钮出现")
        except PlaywrightTimeoutError:
            logs.info("未捕获到停止按钮，可能模型回复较快或停止按钮定位不稳定")
        # 断言语音按钮显示（等待模型回复完成），记录日志
        expect(AIDP.voice_button).to_be_visible(timeout=1000000)
        logs.info("语音按钮显示")
        # 获取提问大模型文本和模型回复文本
        new_count = AIDP.message_items.count()
        latest_message_answer_new = AIDP.message_items.nth(new_count - 1)
        question = latest_message_question.inner_text().strip()
        answer = latest_message_answer_new.inner_text().strip()
        # 断言模型回复不为空，记录日志，并截图
        expect(latest_message_answer_new).to_contain_text(re.compile(r"\S+"), timeout=30000)
        logs.info("模型回答不为空")
        page.screenshot(path=f"./test_results/ai_dialogue_record/chat_message_regenerate2.jpg")
        user_chat_info_write(question, answer, r".\test_results\ai_dialogue_record\chat_message_regenerate.txt")
        logs.info("重新生成完毕")

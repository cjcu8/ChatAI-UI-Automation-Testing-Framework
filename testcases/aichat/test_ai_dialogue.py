import re

import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

from common.get_json_data import get_json_data
from common.log_utils import logs
from common.settings import BASE_DIR
from common.userchat_info_write import user_chat_info_write
from pages.ai_dialogue_page import AIDialoguePage


class TestAIDialogue:

    @pytest.mark.parametrize("test,assert_text,png_name", get_json_data("./data/ai_dialogue_data.json"))
    def test_01_ai_dialogue(self, logged_in_page, test, assert_text, png_name):
        """
        测试用户聊天模块
        """
        page = logged_in_page
        # 创建AI聊天对象
        AIDP = AIDialoguePage(page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(AIDP.chat_input).to_be_visible(timeout=100000)
        # 输入问题，提问大模型
        AIDP.input_text(test)
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
        # 获取提问大模型文本和模型回复文本
        question = latest_message_question.inner_text().strip()
        answer = latest_message_answer.inner_text().strip()
        # 断言模型回复不为空，记录日志，并截图
        if assert_text == "not_empty":
            expect(latest_message_answer).to_contain_text(re.compile(r"\S+"), timeout=30000)
            logs.info("模型回答不为空")
        else:
            expect(latest_message_answer).to_contain_text(assert_text, timeout=30000)
            logs.info(f"模型回答包含预期文本：{assert_text}")
        page.screenshot(path=f"./test_results/ai_dialogue_record/{png_name}")
        user_chat_info_write(question, answer, r".\test_results\ai_dialogue_record\chat_result.txt")

    def test_02_ai_file_dialogue(self, logged_in_page):
        """
        测试用户聊天模块
        """
        page = logged_in_page
        # 创建AI聊天对象
        AIDP = AIDialoguePage(page)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(AIDP.chat_input).to_be_visible(timeout=100000)
        logs.info("首页加载成功")
        AIDP.click_upload_file(BASE_DIR / "data" / "chatfile" / "re_question")
        logged_in_page.wait_for_timeout(3000)
        # 断言文件上传成功
        expect(page.get_by_text("re_question", exact=True)).to_be_visible(timeout=30000)
        # expect(AIDP.stop_button).to_have_count(2, timeout=10000)
        logs.info("文件上传成功")
        # 输入问题，提问大模型
        AIDP.input_text("帮我看看这个文件中的代码的作用是啥？")
        # 断言发送按钮显示，并记录日志
        expect(AIDP.send_button).to_be_visible(timeout=10000)
        logs.info("发送按钮显示")
        AIDP.click_send()
        # 断言语音按钮通常会隐藏，记录日志
        expect(AIDP.voice_button).to_be_hidden(timeout=10000)
        logs.info("语音按钮隐藏")
        # 断言语音按钮显示（等待模型回复完成），记录日志
        expect(AIDP.voice_button).to_be_visible(timeout=1000000)
        logs.info("语音按钮显示")
        # 通过定位消息盒子，获取提问大模型和大模型回复的数量
        old_count = AIDP.message_items.count()
        # 定位提问大模型文本
        latest_message_question = AIDP.message_items.nth(old_count - 2)
        # 定位大模型回复文本
        latest_message_answer = AIDP.message_items.nth(old_count - 1)
        # 获取提问大模型文本和模型回复文本
        question = latest_message_question.inner_text().strip()
        answer = latest_message_answer.inner_text().strip()
        # 断言模型回复不为空，记录日志，并截图
        expect(latest_message_answer).to_contain_text(re.compile(r"\S+"), timeout=30000)
        logs.info("模型回答不为空")
        page.screenshot(path=f"./test_results/ai_dialogue_record/model_file_response.png")
        user_chat_info_write(question, answer, r".\test_results\ai_dialogue_record\chat_file_result.txt")

import re
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from common.log_utils import logs
from common.userchat_info_write import user_chat_info_write
from pages.ai_question_answering_process_page import AIQuestionAnsweringProcessPage


class TestUserChatProcess:

    def test_user_chat_process(self, before_all, login_page):
        """
        测试用户聊天流程
        """
        # 登录
        login_page.login("admin@163.com", "AaAa123456", "/auth")
        # 创建聊天对象
        userchat = AIQuestionAnsweringProcessPage(before_all)
        # 断言登录成功，记录日志，并截图/通过钩子函数自动记录单眼失败日志并截图
        expect(userchat.chat_input).to_be_visible(timeout=100000)
        before_all.screenshot(path="./test_results/aichat_process_record/login_success.png")
        logs.info("登录成功")
        # 切换模型
        # 选择千问大模型
        # 将其设置为默认大模型
        userchat.modelselect()
        userchat.select_qwen_model()
        userchat.set_qwen_default_model()
        # 断言模型更换成功，记录日志，并截图
        expect(userchat.model_update_text).to_contain_text("默认模型已更新")
        before_all.screenshot(path="./test_results/aichat_process_record/model_select_success.png")
        logs.info("模型更换成功")
        # 输入问题，提问大模型
        userchat.input_text("你是谁？")
        # 断言发送按钮显示，并记录日志
        expect(userchat.send_button).to_be_visible(timeout=10000)
        logs.info("发送按钮显示")
        userchat.click_send()
        # 断言语音按钮通常会隐藏，记录日志
        expect(userchat.voice_button).to_be_hidden(timeout=10000)
        logs.info("语音按钮隐藏")
        # 模型生成时，停止按钮应该出现，但不是必须得，因为停止按钮可能定位不到
        try:
            expect(userchat.stop_button).to_be_visible(timeout=1000000)
            logs.info("停止按钮出现")
        except PlaywrightTimeoutError:
            logs.info("未捕获到停止按钮，可能模型回复较快或停止按钮定位不稳定")
        # 断言语音按钮显示（等待模型回复完成），记录日志
        expect(userchat.voice_button).to_be_visible(timeout=1000000)
        logs.info("语音按钮显示")
        # 通过定位消息盒子，获取提问大模型和大模型回复的数量
        old_count = userchat.message_items.count()
        # 定位提问大模型文本
        latest_message_question=userchat.message_items.nth(old_count-2)
        # 定位大模型回复文本
        latest_message_answer=userchat.message_items.nth(old_count-1)
        # 获取提问大模型文本和模型回复文本
        question = latest_message_question.inner_text().strip()
        answer = latest_message_answer.inner_text().strip()
        # 断言模型回复不为空，记录日志，并截图
        expect(latest_message_answer).to_contain_text(re.compile(r"\S+"), timeout=30000)
        before_all.screenshot(path="./test_results/aichat_process_record/model_response.png")
        logs.info("模型回答不为空")
        user_chat_info_write(question, answer,r".\test_results\aichat_process_record\chat_result.txt")




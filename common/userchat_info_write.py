def user_chat_info_write(Question, answer, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write("用户输入：\n")
        f.write(Question)
        f.write("\n\n")
        f.write("模型回复：\n")
        f.write(answer)

import json
from pathlib import Path

# 项目根目录：Open-WebUI
BASE_DIR = Path(__file__).resolve().parent.parent


def get_json_data(file_path):
    """
    读取 JSON 文件数据
    :param file_path: JSON 文件路径
    :return: JSON 文件数据 python类型
    """
    file_path = BASE_DIR / file_path
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data_list = []
        for item in data:
            data_list.append((item.values()))

        return data_list

    except FileNotFoundError:
        raise FileNotFoundError(f"测试数据文件不存在：{file_path}")

    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 文件格式错误：{file_path}，错误信息：{e}")

    except KeyError as e:
        raise KeyError(f"JSON 测试数据缺少字段：{e}")

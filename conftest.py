import allure
import pytest
from pytest import Item
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

from pages.login_page import LoginPage
from common.log_utils import logs


BASE_URL = "http://localhost:5173"
PROJECT_ROOT = Path(__file__).resolve().parent
AUTH_FILE = PROJECT_ROOT / "auth" / "auth_state.json"


@pytest.fixture(scope="session")
def browser():
    """
    整个测试会话只启动一次浏览器
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def auth_state(browser):
    """
    登录一次，并保存登录状态
    """
    if AUTH_FILE.exists():
        print("发现已有登录状态文件，直接复用")
        return str(AUTH_FILE)

    AUTH_FILE.parent.mkdir(exist_ok=True)

    context = browser.new_context(
        no_viewport=True,
        base_url=BASE_URL,
        permissions=["clipboard-read", "clipboard-write"]
    )

    page = context.new_page()
    login = LoginPage(page)
    login.login("admin@163.com", "AaAa123456", url="/auth")

    expect(page.locator("#chat-input")).to_be_visible(timeout=10000)

    context.storage_state(path=str(AUTH_FILE))
    context.close()

    return str(AUTH_FILE)


@pytest.fixture(scope="function")
def logged_in_page(browser, auth_state):
    """
    已登录状态页面，适合不想每个用例都重新登录的测试
    """
    context = browser.new_context(
        no_viewport=True,
        base_url=BASE_URL,
        storage_state=auth_state,
        permissions=["clipboard-read", "clipboard-write"]
    )

    page = context.new_page()
    page.goto("/")

    yield page

    context.close()


@pytest.fixture(scope="function")
def before_all(browser):
    """
    兼容旧用例：提供一个未登录的新页面
    注意：这里不能再写 sync_playwright()
    """
    context = browser.new_context(
        no_viewport=True,
        base_url=BASE_URL,
        permissions=["clipboard-read", "clipboard-write"]
    )

    page = context.new_page()

    yield page

    context.close()


@pytest.fixture(scope="function")
def login_page(before_all):
    """
    登录页面对象
    """
    return LoginPage(before_all)


def pytest_runtest_call(item: Item):
    """
    动态添加 allure feature/title
    """
    if item.parent and getattr(item.parent, "_obj", None):
        if item.parent._obj.__doc__:
            allure.dynamic.feature(item.parent._obj.__doc__)

    if item.function.__doc__:
        allure.dynamic.title(item.function.__doc__)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    用例失败时，自动记录日志并截图
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            logs.error(f"用例执行失败：{item.nodeid}")
            logs.error(f"失败详情：\n{report.longrepr}")

            page = (
                item.funcargs.get("before_all")
                or item.funcargs.get("logged_in_page")
            )

            if page:
                screenshot_dir = Path(
                    "test_results/fail_screenshots"
                )
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = screenshot_dir / f"fail_{current_time}.png"

                page.screenshot(path=str(screenshot_path), full_page=True)

                logs.error(f"失败截图已保存：{screenshot_path}")

        elif report.passed:
            logs.info(f"用例执行通过：{item.nodeid}")
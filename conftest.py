import os

import pytest

FULLHD = {"width": 1920, "height": 1080}

@pytest.fixture(scope="session")
def browser(playwright, pytestconfig):
    """Modifies basic browser fixture from pytest-playwright.
    Ensures start in headed mode, maximized for Chromium.
    """
    browser_name = _get_browser_name(pytestconfig)
    browser = getattr(playwright, browser_name)
    browser_instance = browser.launch(
        headless=False,
        args=(["--start-maximized"] if browser_name == "chromium" else []),
    )
    return browser_instance

def _get_browser_name(pytestconfig):
    browser_name = pytestconfig.getoption("--browser")
    if browser_name:
        browser_name = browser_name[0]
    else:
        browser_name = "chromium"
    return browser_name

def _generate_state_file(pytestconfig, browser):
    """Function to generate state file for authorized state.
    Browser-specific, creates .json file with storage state for specific browser.
    Requires user to manually complete login.
    """
    browser_name = _get_browser_name(pytestconfig)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.instagram.com/")

    with page.expect_event("dialog"):
        page.evaluate("alert('Allow cookies and manually login into website. Resume in Playwright Inspector to continue')")
    page.pause()

    state_file_path = f"{browser_name}_state.json"
    context.storage_state(path=state_file_path)
    print(f"Browser state successfully saved to {state_file_path}.")
    return state_file_path

def _get_state_file(pytestconfig, browser):
    """Get state file for specific browser.
    If file does not exist, runs _generate_state_file to create one.
    """
    browser_name = _get_browser_name(pytestconfig)
    state_file_path = os.path.join(pytestconfig.rootdir, f"{browser_name}_state.json")
    if os.path.exists(state_file_path):
        return state_file_path
    else:
        state_file_path = _generate_state_file(pytestconfig, browser)
        return state_file_path

@pytest.fixture(scope="function")
def context(request, browser, pytestconfig):
    """Ensures browser session is open in FULL HD.
    If test is marked via auth mark, inject authorized state in to storage_state from state_file.
    """
    browser_name = _get_browser_name(pytestconfig)
    if browser_name == "chromium":
        kwargs = {"no_viewport": True}
    else:
        kwargs = {"viewport": FULLHD}
    wants_auth = request.node.get_closest_marker("auth")
    if wants_auth:
        state_file = _get_state_file(pytestconfig, browser)
        kwargs["storage_state"] = state_file
    ctx = browser.new_context(**kwargs)
    yield ctx
    ctx.close()

import re

from playwright.sync_api import expect

from pages.login_page import LoginPage

def test_login_validations(page):
    """Checks basic validations on login page.
    """
    login_page = LoginPage(page)
    login_page.open_page()
    page.get_by_role("progressbar").wait_for(state="hidden")
    if login_page.allow_cookies_button.is_visible():
        login_page.allow_cookies_button.click()
    # Empty inputs
    assert login_page.login_button.is_disabled(), \
        "Submit button should be disabled when username and password inputs are empty."
    login_page.username_input.fill("test")
    assert login_page.login_button.is_disabled(), \
        "Submit button should be disabled when password input is empty."
    # Password length validation
    login_page.password_input.fill("test")
    assert login_page.login_button.is_disabled(), \
        "Submit button should be disabled if password length is less than 6 characters."
    # Wrong password
    login_page.password_input.fill("failtest")
    login_page.login_button.click()
    expected_text = "Sorry, your password was incorrect. Please double-check your password."
    expect(page.locator("body"), "Error message for incorrect password is not found.").to_contain_text(expected_text)
    # Show password
    login_page.password_show_button.click()
    assert login_page.password_input.get_attribute("type") == "text", \
        "Password value is still hidden after 'Show' button press."
    login_page.password_hide_button.click()
    assert login_page.password_input.get_attribute("type") == "password", \
        "Password value is not hidden after 'Hide' button press."

def test_manual_login(page):
    """Checks basic manual login with username/password.
    Can be janky.
    """
    login_page = LoginPage(page)
    login_page.open_page()
    page.get_by_role("progressbar").wait_for(state="hidden")
    if login_page.allow_cookies_button.is_visible():
        login_page.allow_cookies_button.click()
    login_page.username_input.fill("test")
    login_page.password_input.fill("123456")
    login_page.login_button.click()
    page.get_by_role("progressbar").wait_for(state="hidden")
    expected_text = "Help us confirm that it's you"
    expect(page.locator("body"), "Captcha did not open.").to_contain_text(expected_text)

def test_forgot_password(page):
    """Password recovery test.
       Check username validation, sending email and "Can't reset" option
    """
    login_page = LoginPage(page)
    login_page.open_page()
    page.get_by_role("progressbar").wait_for(state="hidden")
    if login_page.allow_cookies_button.is_visible():
        login_page.allow_cookies_button.click()
    login_page.forgot_password_link.click()
    assert login_page.forgot_password_send_button.is_disabled(), "Send button should be inactive when input is empty."
    # Check non-exist username
    login_page.forgot_password_input.fill("testcompletefailure")
    login_page.forgot_password_send_button.click()
    page.locator("p").wait_for(state="visible")
    assert page.locator("p").text_content() == "No users found", "No alert for No users found."
    # Check existing username
    login_page.forgot_password_input.fill("test")
    login_page.forgot_password_send_button.click()
    dialog_window = page.get_by_role("dialog")
    expect(dialog_window, "No dialog about email sent.").to_be_visible()
    assert "email sent" in dialog_window.text_content().lower(), "Wrong dialog window shown."
    # Check "Cannot reset password?" option
    dialog_window.locator("button").click()
    login_page.cannot_reset_password_link.click()
    expect(page).to_have_url(re.compile(".*/accounts/account_recovery/"))

from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.instagram.com/accounts/login/"


    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.cookies_dialog = page.locator(
            "div[role='dialog']", has_text="Allow the use of cookies from Instagram on this browser?")
        self.allow_cookies_button = page.get_by_role("button", name="Allow all cookies")
        self.decline_cookies_button = page.get_by_role("button", name="Decline optional cookies")
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.password_show_button = page.get_by_text("Show")
        self.password_hide_button = page.get_by_text("Hide")
        self.login_button = page.locator("button[type='submit']")
        self.facebook_login_button = page.get_by_role("button", name="Log in with Facebook")
        self.facebook_cookies_dialog = page.locator(
            "div[role='dialog']", has_text="Allow the use of cookies from Facebook on this browser?")
        # self.forgot_password_link = page.get_by_role("link", name="Forgot password?")
        self.forgot_password_link = page.locator("a[role='link']", has_text=" password?")
        self.forgot_password_input = page.locator("input[name='cppEmailOrUsername']")
        self.forgot_password_send_button = page.get_by_role("button", name="Send login link")
        self.cannot_reset_password_link = page.get_by_role("link", name="Can't reset your password?")
        self.report_content_link = page.get_by_role("link", name="report content that you believe is unlawful")
        self.sign_up_link = page.get_by_role("link", name="Sign up")

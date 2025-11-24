from pages.base_page import BasePage

class SignupPage(BasePage):
    URL = "https://www.instagram.com/accounts/emailsignup/"


    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.facebook_login_button = page.get_by_role("button", name="Log in with Facebook")
        self.email_phone_input = page.locator("input[name='emailOrPhone']")
        self.password_input = page.locator("input[name='password']")
        self.full_name_input = page.locator("input[name='fullName']")
        self.username_input = page.locator("input[name='username']")
        self.next_button = page.get_by_role("button", name="Next")
        self.go_back_button = page.get_by_role("button", name="Go back")
        self.login_link = page.get_by_role("link", name="Log in")
        self.month_dropdown = page.locator("select[title='Month:']")# .select_option("June")
        self.day_dropdown = page.locator("select[title='Day:']")# .select_option("13")
        self.year_dropdown = page.locator("select[title='Year:']")# .select_option("2020")
        self.resend_code_button = page.get_by_role("button", name="Resend code.")
        self.code_input = page.locator("input[name='email_confirmation_code']")

from pages.login_page import LoginPage

class UnauthorizedPage(LoginPage):
    URL = "https://www.instagram.com/"

    def __init__(self, page):
        super().__init__(page)
        self.page = page

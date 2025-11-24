from playwright.sync_api import Page

class PostDialog(Page):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.dialog = page.get_by_role("dialog")
        self.dialog_next_button = self.dialog.locator("button[aria-label='Next']")
        self.dialog_previous_button = self.dialog.locator("button[aria-label='Go back']")

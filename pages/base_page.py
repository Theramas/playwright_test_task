from components.sidebar import PageSidebar
from components.article_dialog import ArticleDialog

class BasePage(PageSidebar, ArticleDialog):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def open_page(self):
        self.page.goto(self.URL)

from playwright.sync_api import Page

class PageSidebar(Page):
    """Sidebar menu
    """
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.home_link = page.get_by_role("link", name="Home")
        self.search_link = page.get_by_role("link", name="Search")
        self.explore_link = page.get_by_role("link", name="Explore")
        self.reels_link = page.get_by_role("link", name="Reels")
        self.messages_link = page.get_by_role("link", name="Messages")
        self.notifications_link = page.get_by_role("link", name="Notifications")
        self.create_link = page.get_by_role("link", name="Create")
        self.profile_link = page.get_by_role("link", name="Profile")
        self.more_link = page.get_by_role("link", name="More")
        self.also_from_meta_link = page.get_by_role("link", name="Also from Meta")

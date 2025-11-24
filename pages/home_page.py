import operator

from playwright.sync_api import expect

from pages.base_page import BasePage
from helpers import wait_until

class HomePage(BasePage):
    """Home page wit feed, side bar and suggestions
    """
    URL = "https://www.instagram.com/"

    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.for_you_tab = page.get_by_role("tab", name="For you")
        self.following_tab = page.get_by_role("tab", name="Following")
        self.story_tray = page.locator("div[data-pagelet='story_tray']")
        self.story_element = self.story_tray.locator("li[class='_acaz']")
        self.profile_switch_button = page.get_by_role("button", name="Switch")
        self.main_suggestions_tray = page.locator("xpath=//*[text()='Suggestions for you']//following::ul[@class='_acay']")
        self.main_suggestions_all_link = page.locator("a[href*='/explore/people']")
        self.main_suggestions_next_button = page.locator("button[aria-label='Next']")
        self.main_suggestions_back_button =  page.locator("button[aria-label='Go back']")
        self.feed_article = page.locator("article")

    def get_current_main_suggestions(self):
        """
        Collects elements in Suggestions feed in the middle of the page.
        Finds interactable buttons for each element.
        Returns: list[Locator]: Playwright Locator objects for each element.
        """
        suggestions_elements = self.main_suggestions_tray.locator("li[class='_acaz']").all()
        if suggestions_elements:
            for element in suggestions_elements:
                element.dismiss_button = element.locator("div[aria-label='Dismiss']")
                element.follow_button = element.get_by_role("button", name="Follow")
                element.following_button = element.get_by_role("button", name="Following")
        return suggestions_elements

    def get_current_articles(self, following=False):
        """
        """
        if following:
            self.following_tab.click()
        articles = self.feed_article.all()
        for article in articles:
            article.more_options_button = article.get_by_role("button", name="More Options")
            article.follow_button = article.get_by_role("button", name="Follow")
            article.like_button = article.get_by_role("button", name="Like")
            article.comment_button = article.get_by_role("button", name="Comment")
            article.share_button = article.get_by_role("button", name="Share")
            article.save_button = article.get_by_role("button", name="Save")
            article.emoji_button = article.get_by_role("button", name="Emoji")
            article.channel_link = article.get_by_role("link").nth(1)
            article.post_time = article.locator("time")
            article.likes_count = article.get_by_role("link").nth(3)
            article.more_text_button = article.locator("*[role='button']", has_text="more").nth(2)
            article.view_all_comments_link = article.locator("a[role='link']", has_text="View all")
            article.comment_input = article.locator("textarea")
            article.comment_post_button = article.get_by_role("button", name="Post")
            article.next_image_button = article.locator("button[aria-label='Next']")
            article.previous_image_button = article.locator("button[aria-label='Go back']")
        return articles

    def infinite_scroll(self):
        self.feed_article.all()[-1].scroll_into_view_if_needed()
        position = self.page.get_by_role("progressbar").bounding_box()
        wait_until(self.page.get_by_role("progressbar").bounding_box, condition=position, reverse=True)
        articles = self.get_current_articles()
        return articles

    def get_article_images(self, article):
        while article.next_image_button.is_visible():
            article.next_image_button.click()
        images = article.locator("img").all()
        profile_image = images[0]
        post_images = images[1:]
        return profile_image, post_images

    def get_all_comments(self, article):
        article.view_all_comments_link.scroll_into_view_if_needed()
        article.view_all_comments_link.wait_for(state="visible")
        article.view_all_comments_link.click()
        self.dialog.locator("header").wait_for(state="visible")
        wait_until(self.dialog.locator("ul").count, count=2)
        for _ in range(100):
            comments = self.dialog.locator("ul").all()[1:]
            comments[-1].scroll_into_view_if_needed()
            if self.dialog_more_comments_button.all():
                try:
                    self.dialog_more_comments_button.click(timeout=5000)
                    expect(self.page.get_by_role("progressbar")).to_have_count(0)
                except:
                    break
            else:
                break
        for comment in comments:
            comment.reply_button = comment.locator("button").filter(has_text="Reply")
            comment.like_button = comment.locator("button").filter(has_text="Like")
            comment.likes_button = comment.locator("button").filter(has_text=" likes")
            comment.post_time = comment.locator("time")
        self.page.keyboard.press("Escape")
        return comments

    def add_comment(self, article, comment_text):
        article.comment_input.fill(comment_text)
        article.comment_post_button.click()
        wait_until(self.page.get_by_role("progressbar").count, condition=operator.eq, count=1)

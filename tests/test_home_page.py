import re

import pytest

from pages.home_page import HomePage

@pytest.mark.auth
def test_infinite_scroll(page):
    """Check that infinite scroll works and loads new posts.
    """
    homepage = HomePage(page)
    homepage.open_page()
    art1 = homepage.infinite_scroll()
    first_articles = [art.text_content() for art in art1]
    art2 = homepage.infinite_scroll()
    second_articles = [art.text_content() for art in art2]
    assert not all(art in second_articles for art in first_articles), "Newer posts did not load"
    for _ in range(3):
        last_articles = homepage.infinite_scroll()
    last_articles = [art.text_content() for art in last_articles]
    assert not any(art in last_articles for art in first_articles), "Feed did not update complete with new posts."

@pytest.mark.auth
def test_add_comments(page):
    """Test adding new comment in feed.
    """
    homepage = HomePage(page)
    homepage.open_page()
    # Add comment from feed
    articles = homepage.get_current_articles()
    a1 = articles[0]
    comment_text = "Looks good to me!"
    homepage.add_comment(a1, comment_text)
    assert comment_text in a1.text_content(), "Comment was not added."

@pytest.mark.auth
def test_like_share_subscribe(page):
    """Checks Like/Unlike, Follow/Unfollow and Share features.
    Limited Share test, check only copying to clipboard.
    """
    homepage = HomePage(page)
    homepage.open_page()
    a1 = None
    for _ in range(3):
        articles = homepage.get_current_articles()
        for article in articles:
            likes_text = article.likes_count.text_content()
            result = re.match("(\d+) likes", likes_text)
            if result:
                a1 = article
                break
        else:
            homepage.infinite_scroll()
    # Like
    old_likes = int(a1.likes_count.text_content().strip(" likes"))
    a1.like_button.click()
    new_likes = int(a1.likes_count.text_content().strip(" likes"))
    assert new_likes == old_likes + 1, "Like did not register."
    a1.like_button.click()
    new_likes = int(a1.likes_count.text_content().strip("likes"))
    assert new_likes == old_likes, "Unlike did not register."
    # Share
    a1.share_button.click()
    page.get_by_role("button", name="Copy Link").wait_for(state="visible")
    page.get_by_role("button", name="Copy Link").click()
    page.locator("p").wait_for(state="visible")
    assert page.locator("p").text_content() == "Link copied to clipboard.", "Link was not copied to clipboard."
    page.keyboard.press("Escape")
    # Subscribe
    for _ in range(3):
        unsub_articles = [art for art in homepage.get_current_articles() if art.follow_button.is_visible()]
        if unsub_articles:
            a1 = unsub_articles[0]
            break
        else:
            homepage.infinite_scroll()
    a1.follow_button.click()
    assert a1.follow_button.text_content() == "Following", "Subscribe did not trigger."
    a1.follow_button.click()
    page.get_by_role("button", name="Unfollow").click()
    assert a1.follow_button.text_content() == "Follow", "Unsubscribe did not trigger."

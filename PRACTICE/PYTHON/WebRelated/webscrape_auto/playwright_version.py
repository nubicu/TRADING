from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # launch a real browser (headless=False means you can SEE it)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # navigate to a URL
    page.goto("https://news.ycombinator.com")

    # find elements and interact with them
    page.click("a.morelink")                    # click the "More" link
    page.wait_for_load_state("networkidle")     # wait for page to settle

    # now scrape the new page
    titles = page.query_selector_all(".titleline a")
    for title in titles:
        print(title.inner_text())

    browser.close()

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://example-login.com")

    # fill in form fields
    page.fill("input[name='username']", "your_username")
    page.fill("input[name='password']", "your_password")

    # click the submit button
    page.click("button[type='submit']")

    # wait for navigation
    page.wait_for_url("**/dashboard")
    print("Logged in successfully!")

    browser.close()
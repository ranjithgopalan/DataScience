from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()

    # Navigate to the webpage
    page = context.new_page()
    page.goto("https://pcgcustomer.aig.com/login")

    # Take a screenshot
    page.screenshot(path="screenshot.png")

    # Validate login fields
    assert page.query_selector("input[name='username']")
    assert page.query_selector("input[name='password']")

    # Close the browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
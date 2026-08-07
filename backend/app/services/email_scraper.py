import re
from playwright.async_api import Page

async def scrape_email(page:Page, url):
    """
        Navigate to website url and perform a search for email.
    """
    # Regex pattern for email extraction (compiled as a raw string)
    regex = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

    if not page:
        raise Exception("Browser has not been launched. Call launch_browser() first.")

    # 1. Validate URL to prevent empty or invalid string navigation errors
    if not url or not isinstance(url, str) or not url.strip() or url.startswith("about:"):
        # print(f"Skipping: Invalid or empty URL provided ({url})")
        return None

    url = url.strip()

    try:
        # print(f"Navigating to {url}...")
        # Go to Google Maps
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)

        # Safe networkidle wait (won't crash if it times out)
        try:
            await page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

        # Take screenshot for debugging
        await page.screenshot(path="screenshots/website_loaded.png")

        # Forcefully remove the modal container element from the DOM
        await page.evaluate("""() => {
            // 1. Find the modal backdrop or content wrapper and delete it
            // (Targeting common layout selectors used for overlays)
            const elementsToRemove = document.querySelectorAll("div[class*='modal'], div[class*='popup'], div[class*='overlay']");
            elementsToRemove.forEach(el => el.remove());
            
            // 2. Unfreeze the page scrolling if the popup disabled it
            document.body.style.setProperty('overflow', 'auto', 'important');
            document.documentElement.style.setProperty('overflow', 'auto', 'important');
        }""")

        # Retrieve the complete HTML content of the page
        html_content = await page.content()
            
        # Find all unique emails matching the regex
        emails = set(regex.findall(html_content))
        # print(f"Found {len(emails)} emails.")

        # 2. Safely return an email if found, otherwise return None
        if emails:
            return emails.pop()
        else:
            return ""
    except Exception:
        # print(f"Failed to scrape email from {url}: {e}")
        pass
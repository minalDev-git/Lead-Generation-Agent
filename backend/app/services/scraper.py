import json
import asyncio
from playwright.async_api import Page
from config import CONSOLE
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.status import Status
from services.selectors import CARD_SELECTOR,BUSINESS_NAME,WEBSITE_SELECTOR,PHONE_SELECTOR,ADDRESS_SELECTOR,RESULTS_PANEL
from services.email_scraper import scrape_email
from urllib.parse import urlparse

console = CONSOLE

SKIP_DOMAINS = {
    "facebook.com",
    "www.facebook.com",
    "instagram.com",
    "www.instagram.com",
    "linktr.ee",
}

async def wait_for_panel_update(page: Page, previous_name: str, timeout_ms: int = 8000) -> str:
    """
    Polls the detail panel's name element until its text differs from the
    previously-scraped business name, confirming the sidebar has actually
    updated to the newly clicked card.
    """
    name_locator = page.locator(BUSINESS_NAME).first
    poll_interval_s = 0.15
    elapsed_ms = 0

    while elapsed_ms < timeout_ms:
        if await name_locator.count() > 0:
            try:
                current = (await name_locator.inner_text()).strip()
            except Exception:
                current = ""
            if current and current != previous_name.strip():
                return current
        await asyncio.sleep(poll_interval_s)
        elapsed_ms += int(poll_interval_s * 1000)

    # Timed out — return whatever's currently there so caller can decide
    if await name_locator.count() > 0:
        try:
            return (await name_locator.inner_text()).strip()
        except Exception:
            return ""
    return ""


async def scrape_businesses(page: Page, status: Status | None = None):
    businesses = []
    processed_count = 0
    max_scroll_attempts = 10
    no_new_cards_count = 0
    previous_name = ""  # tracks last-confirmed panel name
    MAX_RESULTS = 40

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=True,
        refresh_per_second=4,
    ) as progress:
        task = progress.add_task("[cyan]Scraping leads[/]", total=MAX_RESULTS)

        while no_new_cards_count < max_scroll_attempts and processed_count < MAX_RESULTS:
            current_card_count = await page.locator(CARD_SELECTOR).count()

            if processed_count >= current_card_count:

                await page.locator(RESULTS_PANEL).evaluate("(node) => node.scrollTo(0, node.scrollHeight)")
                await asyncio.sleep(2)

                new_count = await page.locator(CARD_SELECTOR).count()
                if new_count == current_card_count:
                    no_new_cards_count += 1
                else:
                    no_new_cards_count = 0
                continue

            card = page.locator(CARD_SELECTOR).nth(processed_count)

            try:
                await card.scroll_into_view_if_needed()
                await card.click()

                # Wait for the panel to actually change, not just be "visible"
                business_name = await wait_for_panel_update(page, previous_name)

                if not business_name or business_name == previous_name:
                    pass
                else:
                    phone_element = page.locator(PHONE_SELECTOR)
                    phone = await phone_element.first.inner_text() if await phone_element.count() > 0 else ""
                    
                    address_element = page.locator(ADDRESS_SELECTOR)
                    address = await address_element.first.inner_text() if await address_element.count() > 0 else ""

                    website_element = page.locator(WEBSITE_SELECTOR)
                    website = await website_element.first.get_attribute("href") if await website_element.count() > 0 else ""

                    domain = urlparse(website).netloc.lower()
                    if domain in SKIP_DOMAINS:
                        email = ""
                    else:
                        website_page = await page.context.new_page()
                        email = await scrape_email(website_page, website)
                        await website_page.close()
                        if not email:
                            email = ""

                    business_data = {
                        "name": business_name,
                        "website": website,
                        "phone": phone,
                        "address": address,
                        "email": email
                    }

                    businesses.append(business_data)
                    previous_name = business_name

            except Exception:
                pass

            finally:
                processed_count += 1
                progress.advance(task)

    max_items = 3
    truncated_list = businesses[:max_items]

    # 2. Pretty-print it to the terminal
    console.print(f"--- Tool Output Preview ({len(truncated_list)} of {len(businesses)} collected, previewing {len(truncated_list)}) ---")
    console.print_json(json.dumps(truncated_list, indent=2))
    return businesses

# THIS FUNCTION WAS IMPLEMENTED BEFORE ADDING BATCHED LOGIC TO LOAD ALL THE CARDS

# async def scrape_businesses(page: Page):

#     businesses = []

#     await page.locator(CARD_SELECTOR).first.wait_for()

#     business_cards = await page.locator(CARD_SELECTOR).all()

#     print(f"Discovered {len(business_cards)} business cards on screen.")

#     for index, card in enumerate(business_cards):
#         await card.click()
#         try:
#             # 1. Extract Business Name
#             name_element = page.locator(BUSINESS_NAME)
#             await name_element.first.wait_for(timeout=5000)
#             business_name = await name_element.first.inner_text() if await name_element.count() > 0 else ""

#             # 2. Extract Website URL (if available)
#             website_element = page.locator(WEBSITE_SELECTOR)
#             if await website_element.count() > 0:
#                 website = await website_element.first.get_attribute("href")
#             else:
#                 website = ""

#             # 3. Extract Phone Number (if available)
#             phone_element = page.locator(PHONE_SELECTOR)
#             if await phone_element.count() > 0:
#                 phone = await phone_element.first.inner_text()
#             else:
#                 phone = ""

#             address_element = page.locator(ADDRESS_SELECTOR)

#             if await address_element.count() > 0:
#                 address = await address_element.first.inner_text()
#             else:
#                 address = ""

#             businesses.append({
#                 "name": business_name,
#                 "website": website,
#                 "phone": phone,
#                 "address": address
#             })

#         except Exception as e:
#             print(f"Skipping card {index}: {e}")
#             continue

#     return businesses
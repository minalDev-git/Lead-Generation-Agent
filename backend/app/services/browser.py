import asyncio
from playwright.async_api import async_playwright, Page
from config import CONSOLE
from rich.status import Status
from services.selectors import GOOGLE_MAPS_SEARCH_BOX, RESULTS_PANEL
from config import HEADLESS
from services.scraper import scrape_businesses

console = CONSOLE

async def search_google_maps(page: Page, business_type: str, location: str, status: Status | None = None):
    """
    Navigate to Google Maps and perform a search using the extracted business type and location.
    """
    if not page:
        raise Exception("Browser has not been launched. Call launch_browser() first.")

    query = f"{business_type} in {location}"
    if status:
        status.update(f"[bold cyan]Navigating to Google Maps[/]")
        status.update(f"[bold cyan]Typing search query:[/] [yellow]{query}[/]")

    # Go to Google Maps
    await page.goto(
        "https://www.google.com/maps",
        wait_until="domcontentloaded",
        timeout=60000
    )
    # Take screenshot for debugging
    # await page.screenshot(path="screenshots/01_maps_loaded.png")
    # Type search query into Google Maps input
    search_box = page.locator(GOOGLE_MAPS_SEARCH_BOX)

    await search_box.wait_for()
    await search_box.fill(query)
    await search_box.fill(query)

    # Take screenshot for debugging
    # await page.screenshot(path="screenshots/02_query_typed.png")
    await search_box.press("Enter")

    # # Wait for results panel to render
    await page.wait_for_load_state("domcontentloaded")
    await page.wait_for_selector(RESULTS_PANEL, timeout=30000)
    if status:
        status.update("[bold green]Search results loaded[/]")

    # return scrapped businesses
    businesses = await scrape_businesses(page, status=status)
    return businesses

async def close_browser(browser):
    try:
        if browser and browser.is_connected():
            await asyncio.wait_for(browser.close(), timeout=1000)
    except Exception as e:
        print(f"Browser close failed: {e}")

async def scrape_leads(business_type: str, location: str,headless: bool = HEADLESS) -> list[dict]:
    """
    Start Playwright, Launch Chromium, Create Context, and Open New Page.
    """
    console.log(f"[bold blue]Starting Google Maps lead scraping for[/] [yellow]{business_type}[/] [bold blue]in[/] [yellow]{location}[/]")
    # --- Start Playwright ---
    async with async_playwright() as playwright:

        # --- Launch Chromium ---
        with console.status("[bold green]Launching browser and preparing your search...[/]", spinner="dots") as status:
            status.update("[bold cyan]Launching Chromium[/]")
            browser = await playwright.chromium.launch(slow_mo=500,headless=headless)

            # --- Create Context ---
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            # --- Open New Page ---
            page = await context.new_page()

            try:
                status.update(f"[bold cyan]Searching for [yellow]{business_type} in {location}[/]...[/]")
                businesses = await search_google_maps(page, business_type,location, status=status)
                return businesses
            finally:
                await close_browser(browser)
                # async with exit stops playwright exactly once, here


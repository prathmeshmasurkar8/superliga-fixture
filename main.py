import nest_asyncio
nest_asyncio.apply()

from playwright.async_api import async_playwright

async def run_scraper():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.flashscore.in/football/romania/superliga/fixtures/", timeout=30000)

        # Wait for matches to load
        await page.wait_for_selector("div.event__match", timeout=20000)
        await page.wait_for_timeout(3000)  # extra wait for JS

        matches = await page.query_selector_all("div.event__match")
        print(f"Found {len(matches)} matches")

        for match in matches:
            time_el = await match.query_selector(".event__time")
            time = await time_el.inner_text() if time_el else "N/A"

            home_el = await match.query_selector("div.event__homeParticipant span.wcl-name_3y6f5")
            home = await home_el.inner_text() if home_el else "N/A"

            away_el = await match.query_selector("div.event__awayParticipant span.wcl-name_3y6f5")
            away = await away_el.inner_text() if away_el else "N/A"

            print(f"{time} - {home} vs {away}")

        await browser.close()

await run_scraper()

import json
from pathlib import Path

from sites import BaseSite
from sites.google import Google

from browser_use import Browser

class Partiful(BaseSite):
    name = "Partiful"
    url = "https://partiful.com"
    logo_url = "https://partiful.com/favicon.ico"
    
    browser: Browser

    async def get_parties(self, city_code: str = "sf"):
        await self.start()
        await self.browser.navigate_to(f"{self.url}/explore/{city_code}")
        parties = []
        page = await self.browser.get_current_page()
        if page:
            party_links = await page.get_elements_by_css_selector("a[href*='/e/']")
            parties = [await link.get_attribute("href") for link in party_links]
        await self.stop()
        return parties

    async def get_rsvped(self, party_url: str):
        rsvped = []
        har_path = Path("./traces/partiful.har")
        if har_path.exists():
            har_path.unlink()

        await self.start(record_har_path=str(har_path), record_har_content="embed")
        await self.browser.navigate_to(f"{self.url}/{party_url}")
        await self.stop()

        if not har_path.exists():
            return rsvped

        har_data = json.loads(har_path.read_text())
        google = Google()
        
        response = await google.ask_gemini(f"Extract the names of the people who RSVPed to the party at {party_url} on Partiful based on the following HAR data:", uploaded_files=[str(har_path)])
        print(f"Gemini response: {response}")
        return response
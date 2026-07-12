import re
import asyncio
from pathlib import Path
from sites import BaseSite

from browser_use import Browser

class Google(BaseSite):
    name = "Google"
    url = "https://google.com/aimode"
    logo_url = "https://google.com/favicon.ico"
    
    browser: Browser

    async def ask_gemini(self, prompt: str, uploaded_files: list[str] = []):
        har_path = Path("./traces/google.har")
        if har_path.exists():
            har_path.unlink()

        await self.start(cloud_timeout=10)
        await self.browser.navigate_to(f"{self.url}")
        page = await self.browser.get_current_page()

        response = ""
        if page:
            search_box = await page.get_elements_by_css_selector("textarea")
            if search_box:
                print("Found search box, sending prompt...")
                box = search_box[0]
                await box.fill(f"{prompt}. Please start your answer with 'AAnswer:' and end it with 'AEnd.'") 
                
                await page.press("Enter")
                await asyncio.sleep(60)  # Wait for response to generate
                
                page_text = await page.evaluate("() => document.body.innerText")
                matches = re.findall(r"AAnswer:(.*?)AEnd\.", page_text, re.DOTALL)
                print(f"extracted Gemini answer: {"".join(match.strip() for match in matches) if matches else 'No match found'}")
                response = matches[-1].strip() if matches else None
                print(f"received response from Gemini: {response}")
                    
        await self.stop()
        return response
  
    #TODO: Eman 
    async def validate_job_link(link: str):
        #navigate to link, check if its the actual job description page with apply button
        return
import re
import json
import asyncio
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, TypeVar

from sites import BaseSite
from browser_use import Browser

T = TypeVar('T', bound=BaseModel)
class Google(BaseSite):
    name = "Google"
    url = "https://google.com/aimode"
    logo_url = "https://google.com/favicon.ico"
    
    browser: Browser

    async def ask_gemini(self, prompt: str, timeout: int = 60) -> Optional[str]:
        har_path = Path("./traces/google.har")
        if har_path.exists():
            har_path.unlink()

        await self.start(cloud_timeout=20)
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
                await asyncio.sleep(timeout)  # Wait for response to generate
                
                page_text = await page.evaluate("() => document.body.textContent")
                matches = re.findall(r"AAnswer:(.*?)AEnd\.", page_text, re.DOTALL)
                response = re.sub(r'use code with caution\.', '', matches[-1].strip().replace('json', ''), flags=re.IGNORECASE) if matches else None
                print(f"Gemini returned: {response}")
        await self.stop()
        return response
    
    async def ask_gemini_json(self, prompt: str, output_format: type[T], timeout: int = 60) -> Optional[List[T]]:
        response = await self.ask_gemini(prompt, timeout=timeout)
        response = json.loads(response) if response else None
        if isinstance(response, list):
            for i in range(len(response)):
                try:
                    response[i] = output_format(**response[i])
                except:
                    print(f"Failed to parse {response[i]} into {output_format}")
        else:
            print(f"Expected list, got: {response}")
        return response 
    
    # #TODO: Eman 
    # async def validate_job_link(link: str):
    #     #navigate to link, check if its the actual job description page with apply button
    #     return
    
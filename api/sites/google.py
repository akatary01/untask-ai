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

    async def ask_gemini(self, prompt: str, timeout: int = 120) -> Optional[str]:
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
                if response == "":
                    return await self.ask_gemini(prompt, timeout=timeout) 
        await self.stop()
        return response
    
    async def ask_gemini_json(self, prompt: str, output_format: type[T], timeout: int = 120) -> Optional[List[T]]:
        try:
            response = await self.ask_gemini(prompt, timeout=timeout)
            
            if not response: # handling non response
                print("Gemini returned empty string")
                return None
            # 3. Proceed to Parse JSON safely
            response_data = json.loads(response)
        
            if isinstance(response_data, list):
                return [output_format(**item) for item in response_data]
            else:
                print(f"Expected list layout, but JSON parsed into a: {type(response_data)}")
                return None
        
        except json.JSONDecodeError:
            print("Failed to decode JSON")
            return None
        except asyncio.TimeoutError:
            print(f"The request timed out locally after {timeout} seconds.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    
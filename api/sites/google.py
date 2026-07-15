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

    async def ask_gemini(self, prompt: str, timeout: int = 180) -> Optional[str]:
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
    
    async def ask_gemini_json(self, prompt: str, output_format: type[T], timeout: int = 120) -> Optional[List[T]]:
        try:
            response = await self.ask_gemini(prompt, timeout=timeout)
            print(f"gemini response: {type(response)}, content: '{response}'")

            if(not response): #handling non response
                print("Gemini returned empty string")
                return None
            if hasattr(response, "candidates") and response.candidates:
                finish_reason = response.candidates[0].finish_reason
                # Check if it was stopped by safety filters, recitation blocking, etc.
                if finish_reason not in ["STOP", 1, None]:  
                    print(f"Warning: Gemini stopped generating. Reason: {finish_reason}")
        
            if hasattr(response, "prompt_feedback") and getattr(response.prompt_feedback, "block_reason", None):
                print(f"Prompt Blocked: {response.prompt_feedback.block_reason}")
                return None      
            
            content_text = response.text if hasattr(response, "text") else str(response)
            
            if not content_text.strip():
                print("Gemini returned successfully but the text content block was blank.")
                return None

            # 3. Proceed to Parse JSON safely
            response_data = json.loads(content_text)
        
            if isinstance(response_data, list):
                return [output_format(**item) for item in response_data]
            else:
                print(f"Expected list layout, but JSON parsed into a: {type(response_data)}")
                return None
        
        except json.JSONDecodeError:
            print(f"Failed to decode JSON. Raw content was: {content_text}")
            return None
        except asyncio.TimeoutError:
            print(f"The request timed out locally after {timeout} seconds.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        
    
    # #TODO: Eman 
    # async def validate_job_link(link: str):
    #     #navigate to link, check if its the actual job description page with apply button
    #     return
    
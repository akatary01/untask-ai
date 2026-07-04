from typing import Optional
from browser_use import Browser

class BaseSite:
    url: str
    name: str 
    browser: Browser
    
    async def start(self, **kwargs):
        self.browser = Browser(
            cloud_proxy_country_code=kwargs.pop('cloud_proxy_country_code', 'us'), 
            cloud_timeout=kwargs.pop('cloud_timeout', 3), 
            timeout=kwargs.pop('timeout', 10),
            **kwargs,
        )
        await self.browser.start()

    async def start_recorded(self, har_path: str, **kwargs):
        await self.start(record_har_path=har_path, record_har_content='embed', **kwargs)
    
    async def stop(self):
       await self.browser.stop()
    
    
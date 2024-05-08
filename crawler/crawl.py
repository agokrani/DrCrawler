import json
import fnmatch
from urllib.parse import urlparse, urljoin
from playwright.async_api import async_playwright, TimeoutError
from .config import Config

class Crawler: 
    def __init__(self, config: Config):
        self.config = config
    
    async def get_page_html(self, page):
        try:
            # Wait for the selector to appear, with a maximum wait time of 3 seconds
            await page.wait_for_selector(self.config.selector, timeout=3000)
            element = await page.query_selector(self.config.selector)
            return await element.inner_text() if element else ""
        except TimeoutError:
            # Return an empty string if the selector times out
            return ""

    async def crawl(self):
        results = []
        queue = [self.config.url] # Initialize the queue with the initial URL
        visited_urls = set() # Track visited URLs to prevent revisiting
        page_count = 0 # Track the number of pages crawled

        # Initialize Playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Add a cookie if specified in the configuration
            if self.config.cookie:
                await page.context.add_cookies([{
                    "name": self.config.cookie['name'],
                    "value": self.config.cookie['value'], "url": self.config.url}])
            try: 
                while queue and page_count < self.config.max_pages_to_crawl:
                    url = queue.pop(0)
                    cleaned_url = url.split('#')[0]
                    if cleaned_url in visited_urls:
                        continue
                    visited_urls.add(cleaned_url)
                    try:
                        # Attempt to access the page, setting a timeout of 3 seconds
                        await page.goto(cleaned_url, timeout=3000)
                        html = await self.get_page_html(page)
                        if html:  # Only add to results if HTML content was successfully retrieved
                            results.append({'url': cleaned_url, 'html': html})
                            page_count += 1
                            print(f"Crawler: Crawling Page {page_count} at {cleaned_url}")
                        
                        
                    except TimeoutError:
                        print(f'Timeout error occurred while trying to load {cleaned_url}')
                    
                
                    links = await page.query_selector_all("a")
                    #import pdb;pdb.set_trace()
                    for link in links:
                        href = await link.get_attribute("href")
                        if href:
                            full_url = urljoin(cleaned_url, href)
                            # Remove the hash from the URL
                            cleaned_full_url = full_url.split('#')[0]
                            if cleaned_full_url not in visited_urls and fnmatch.fnmatch(cleaned_full_url, self.config.match):
                                queue.append(cleaned_full_url)
            finally: 
                await browser.close()

            return results

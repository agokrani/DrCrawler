import json 
import asyncio
from crawler.config import Config
from crawler.crawl import Crawler

# Main function to initiate the crawling process
async def main(config: Config):
    results = await Crawler(config).crawl()
    with open(config.output_file_name, 'w') as f:
        json.dump(results, f, indent=2)

# Running the main function
if __name__ == "__main__":
    config = Config(
        url="https://www.medindia.net/dr/drjoekaushik",
        match="https://www.medindia.net/dr/**",
        selector="body",
        max_pages_to_crawl=10,
        output_file_name="output.json"
    )
    asyncio.run(main(config))
from .crawler.config import Config
from .crawler.crawl import Crawler

# Main function to initiate the crawling process
async def main(config):
    results = await crawl(config)
    with open(config.output_file_name, 'w') as f:
        json.dump(results, f, indent=2)

# Running the main function
if __name__ == "__main__":
    config = Config(
        url="https://getbootstrap.com/docs/5.3/getting-started/introduction/",
        match="https://getbootstrap.com/docs/5.3/getting-started/**",
        selector="body",
        max_pages_to_crawl=2,
        output_file_name="output.json"
    )
    asyncio.run(main(config))
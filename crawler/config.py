



class Config: 
    def __init__(self, url, match, selector, max_pages_to_crawl, output_file_name, cookie=None):
        """
        Initialization configuration class.

        :param url: str - The initial URL from which the spider starts crawling.
        :param match: str - Pattern string used to match links, typically using wildcards.
        :param selector: str - CSS selector used to extract content from the page.
        :param max_pages_to_crawl: int - Maximum number of pages to crawl to prevent infinite crawling.
        :param output_file_name: str - The JSON file name to which the results are output.
        :param cookie: dict - Optional, dictionary containing cookie information, formatted as {'name': 'cookie_name', 'value': 'cookie_value', 'url': 'cookie_url'}.
        
        """
        self.url = url
        self.match = match
        self.selector = selector
        self.max_pages_to_crawl = max_pages_to_crawl
        self.output_file_name = output_file_name
        self.cookie = cookie
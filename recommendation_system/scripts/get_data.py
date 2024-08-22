from cocktail_scraper import CocktailScraper
from crawl import Crawler

if __name__ == "__main__":
    base_url = ""
    start_url = ""
    scraper = CocktailScraper()
    crawler = Crawler(base_url, start_url, crawl_limit=10)
    crawler.crawl(scraper)

import logging
import time
from collections import deque
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from cocktail_scraper import CocktailScraper
from logs.logger import Logger

Logger.setup_log(log_level=logging.INFO, local_dir="./logs")
logger = logging.getLogger(__name__)


class Crawler:
    def __init__(
        self,
        base_url: str,
        start_url: str,
        user_agent: str = "Mozilla/5.0",
        crawl_limit: int = 10,
    ):
        self.base_url = base_url
        self.start_url = start_url
        self.crawl_limit = crawl_limit
        self.session = requests.Session()
        self.headers = {"User-Agent": user_agent}
        self.visited_urls = set()
        self.nxt_queue = deque([start_url])
        self.prev_queue = deque()
        now = datetime.now().strftime("%m%d%Y_%H%M")
        self.data_path = f"data/{now}/crlmt_{self.crawl_limit}"
        self.model_path = f"model/{now}/crlmt_{self.crawl_limit}"
        Path(self.data_path).mkdir(parents=True, exist_ok=True)
        Path(self.model_path).mkdir(parents=True, exist_ok=True)
        logger.info(
            f"Initialized Crawler with base_url={base_url}, start_url={start_url}, crawl_limit={crawl_limit}"
        )

    def get_soup(self, url: str) -> BeautifulSoup:
        try:
            response = self.session.get(self.base_url + url, headers=self.headers)
            response.raise_for_status()
            logger.debug(f"Successfully fetched URL: {url}")
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Request failed for URL {url}: {e}")
            return None

    def process_queue(self, queue: deque, scraper: "CocktailScraper") -> None:
        while queue and len(scraper.df) < self.crawl_limit:
            current_url = queue.popleft()
            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            logger.info(f"Visiting {current_url}")

            try:
                soup = self.get_soup(current_url)
                if not soup:
                    continue

                scraper.scrape_cocktail_details(soup, current_url)
                previous, nxt = scraper.get_next_cocktails(soup)

                if nxt and nxt not in self.visited_urls:
                    self.nxt_queue.append(nxt)
                if previous and previous not in self.visited_urls:
                    self.prev_queue.append(previous)

                logger.info(
                    f"Processed {current_url}. Total records: {len(scraper.df)}"
                )
                time.sleep(3)

            except Exception as e:
                logger.error(f"Error processing {current_url}: {e}")

            try:
                scraper.df.to_csv(f"{self.data_path}/cocktail_data.csv", index=False)
                logger.info(f"Data saved to {self.data_path}/cocktail_data.csv")
            except Exception as e:
                logger.error(f"Failed to save data: {e}")

    def crawl(self, scraper: "CocktailScraper") -> None:
        try:
            while (self.nxt_queue or self.prev_queue) and len(
                scraper.df
            ) < self.crawl_limit:
                if self.nxt_queue:
                    self.process_queue(self.nxt_queue, scraper)
                if self.prev_queue:
                    self.process_queue(self.prev_queue, scraper)

                if not self.nxt_queue and self.prev_queue:
                    self.nxt_queue, self.prev_queue = self.prev_queue, self.nxt_queue

            try:
                scraper.df.to_csv(f"{self.data_path}/cocktail_data.csv", index=False)
                logger.info(f"Final data saved to {self.data_path}/cocktail_data.csv")
            except Exception as e:
                logger.error(f"Failed to save final data: {e}")

        except KeyboardInterrupt:
            logger.warning("Process interrupted. Saving data...")
            try:
                scraper.df.to_csv(f"{self.data_path}/cocktail_data.csv", index=False)
                logger.info(f"Data saved to {self.data_path}/cocktail_data.csv")
            except Exception as e:
                logger.error(f"Failed to save data after interruption: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            try:
                scraper.df.to_csv(f"{self.data_path}/cocktail_data.csv", index=False)
                logger.info(f"Data saved to {self.data_path}/cocktail_data.csv")
            except Exception as save_error:
                logger.error(f"Failed to save data after error: {save_error}")


if __name__ == "__main__":
    base_url = ""
    start_url = ""
    crawler = Crawler(base_url, start_url)
    crawler.crawl()

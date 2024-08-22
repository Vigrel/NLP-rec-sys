import csv
import time
from collections import deque

import requests
from bs4 import BeautifulSoup
from cocktail_scraper import CocktailScraper


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

    def get_soup(self, url: str) -> BeautifulSoup:
        response = self.session.get(self.base_url + url, headers=self.headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def process_queue(self, queue: deque, scraper: "CocktailScraper") -> None:
        while queue and len(scraper.df) < self.crawl_limit:
            current_url = queue.popleft()
            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            print(f"Visiting {current_url}")

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

                print(f"Processed {current_url}. Total records: {len(scraper.df)}")
                time.sleep(3)  # Throttling to avoid overwhelming the server

            except requests.RequestException as e:
                print(f"Request failed for {current_url}: {e}")
            except Exception as e:
                print(f"Error processing {current_url}: {e}")

            # Save data periodically
            scraper.df.to_csv("data/cocktail_data.csv", index=False)

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

            # Final save
            scraper.df.to_csv("data/cocktail_data.csv", index=False)
            print("Data saved to data/cocktail_data.csv")


        except KeyboardInterrupt:
            print("Process interrupted. Saving data...")
            scraper.df.to_csv("data/cocktail_data.csv", index=False)
            print("Data saved to data/cocktail_data.csv")
        except Exception as e:
            print(f"An error occurred: {e}")
            scraper.df.to_csv("data/cocktail_data.csv", index=False)
            print("Data saved to data/cocktail_data.csv")


if __name__ == "__main__":
    base_url = ""
    start_url = ""
    crawler = Crawler(base_url, start_url)
    crawler.crawl()
